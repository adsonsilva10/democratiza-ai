from typing import List, Dict, Any, Optional, Union, Literal
import asyncio
import openai
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text, and_, or_
from sqlalchemy.orm import selectinload
import numpy as np
from enum import Enum
from app.db.models import KnowledgeBase, LegalDocument, LegalChunk
from app.core.config import settings
import logging

# Multi-provider imports
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)

class EmbeddingProvider(str, Enum):
    """Supported embedding providers for RAG"""
    GEMINI = "gemini"          # Google Gemini (default - free/cheap)
    OPENAI = "openai"          # OpenAI (fallback - best quality)

class RAGService:
    """Multi-provider Retrieval-Augmented Generation service for legal knowledge"""
    
    def __init__(self, provider: Optional[EmbeddingProvider] = None):
        """
        Initialize RAG service with specified embedding provider.
        
        Args:
            provider: Embedding provider to use. If None, auto-selects based on available API keys.
                     Priority: Gemini (free/cheap) > OpenAI (best quality)
        """
        self.provider = provider or self._auto_select_provider()
        self._initialize_provider()
    
    def _auto_select_provider(self) -> EmbeddingProvider:
        """Automatically select best available embedding provider"""
        # Priority 1: Gemini (we have the key and it's free/cheap!)
        google_key = getattr(settings, 'GOOGLE_API_KEY', None)
        if google_key and GEMINI_AVAILABLE:
            logger.info("Auto-selected Gemini embeddings (GOOGLE_API_KEY found)")
            return EmbeddingProvider.GEMINI
        
        # Priority 2: OpenAI (best quality, but needs key)
        openai_key = getattr(settings, 'OPENAI_API_KEY', None)
        if openai_key:
            logger.info("Auto-selected OpenAI embeddings (OPENAI_API_KEY found)")
            return EmbeddingProvider.OPENAI
        
        # Fallback: Try Gemini even without explicit check
        if GEMINI_AVAILABLE:
            logger.warning("No API keys found, attempting Gemini with environment key")
            return EmbeddingProvider.GEMINI
        
        raise ValueError(
            "No embedding provider available. Please set GOOGLE_API_KEY or OPENAI_API_KEY in .env"
        )
    
    def _initialize_provider(self):
        """Initialize the selected embedding provider with appropriate configuration"""
        
        if self.provider == EmbeddingProvider.GEMINI:
            self._initialize_gemini()
        elif self.provider == EmbeddingProvider.OPENAI:
            self._initialize_openai()
        else:
            raise ValueError(f"Unsupported embedding provider: {self.provider}")
    
    def _initialize_gemini(self):
        """Initialize Google Gemini embeddings"""
        google_key = getattr(settings, 'GOOGLE_API_KEY', None)
        if not google_key:
            raise ValueError("GOOGLE_API_KEY not found in settings")
        
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        
        genai.configure(api_key=google_key)
        self.embedding_model = "models/embedding-001"  # Gemini embedding model
        self.embedding_dimension = 768  # Gemini uses 768-dimensional embeddings
        logger.info(f"✅ RAG initialized with Google Gemini embeddings (dimension: {self.embedding_dimension})")
    
    def _initialize_openai(self):
        """Initialize OpenAI embeddings"""
        openai_key = getattr(settings, 'OPENAI_API_KEY', None)
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in settings")
        
        openai.api_key = openai_key
        self.embedding_model = "text-embedding-3-small"  # OpenAI's latest embedding model
        self.embedding_dimension = 1536  # OpenAI uses 1536-dimensional embeddings
        logger.info(f"✅ RAG initialized with OpenAI embeddings (dimension: {self.embedding_dimension})")
    
    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings using the configured provider.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors (dimension varies by provider)
        """
        if self.provider == EmbeddingProvider.GEMINI:
            return await self._create_gemini_embeddings(texts)
        elif self.provider == EmbeddingProvider.OPENAI:
            return await self._create_openai_embeddings(texts)
        else:
            raise ValueError(f"Unknown embedding provider: {self.provider}")
    
    async def _create_gemini_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using Google Gemini"""
        try:
            all_embeddings = []
            
            # Gemini processes one at a time (no batching in API)
            for text in texts:
                result = genai.embed_content(
                    model=self.embedding_model,
                    content=text,
                    task_type="retrieval_document",  # Optimized for RAG
                    title="Legal Contract Document"   # Optional: helps with context
                )
                all_embeddings.append(result['embedding'])
            
            logger.debug(f"Created {len(all_embeddings)} Gemini embeddings")
            return all_embeddings
            
        except Exception as e:
            logger.error(f"Error creating Gemini embeddings: {e}")
            raise
    
    async def _create_openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings using OpenAI"""
        try:
            # Process in batches to handle rate limits
            batch_size = 100
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                
                # Call OpenAI API
                response = await asyncio.get_event_loop().run_in_executor(
                    None,
                    lambda: openai.embeddings.create(
                        input=batch_texts,
                        model=self.embedding_model
                    )
                )
                
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)
            
            logger.debug(f"Created {len(all_embeddings)} OpenAI embeddings")
            return all_embeddings
            
        except Exception as e:
            logger.error(f"Error creating OpenAI embeddings: {e}")
            raise
    
    async def search_legal_knowledge(
        self, 
        query: str, 
        contract_category: Optional[str] = None,
        document_types: Optional[List[str]] = None,
        authority_level: Optional[str] = None,
        limit: int = 10,
        similarity_threshold: float = 0.75,
        db: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """
        Advanced search for legal knowledge using vector similarity
        
        Args:
            query: Search query text
            contract_category: Filter by contract category (locacao, telecom, financeiro, etc.)
            document_types: Filter by document types (lei, jurisprudencia, doutrina, etc.)
            authority_level: Filter by authority level (high, medium, low)
            limit: Maximum number of results per source type
            similarity_threshold: Minimum similarity score
            db: Database session
            
        Returns:
            Structured results with legal chunks and documents
        """
        if not db:
            raise ValueError("Database session is required")
        
        try:
            # Generate query embedding
            query_embeddings = await self.create_embeddings([query])
            query_vector = query_embeddings[0]
            
            # Search in legal chunks for detailed context
            chunks_query = text("""
                SELECT 
                    lc.id, lc.content, lc.chunk_type, lc.chunk_order,
                    lc.section_title, lc.importance_score, lc.legal_concepts,
                    ld.title, ld.document_type, ld.category, ld.source,
                    ld.reference_number, ld.authority_level, ld.publication_date,
                    1 - (lc.embedding <=> :query_vector) as similarity_score
                FROM legal_chunks lc
                JOIN legal_documents ld ON lc.document_id = ld.id
                WHERE lc.is_active = true 
                AND ld.is_active = true
                AND ld.processing_status = 'indexed'
                AND (:contract_category IS NULL OR ld.category = :contract_category)
                AND (:authority_level IS NULL OR ld.authority_level = :authority_level)
                AND (
                    :document_types IS NULL OR 
                    ld.document_type = ANY(string_to_array(:document_types, ','))
                )
                AND 1 - (lc.embedding <=> :query_vector) > :threshold
                ORDER BY 
                    lc.importance_score DESC,
                    ld.authority_level = 'high' DESC,
                    embedding <=> :query_vector
                LIMIT :limit
            """)
            
            chunks_result = await db.execute(
                chunks_query,
                {
                    "query_vector": str(query_vector),
                    "contract_category": contract_category,
                    "authority_level": authority_level,
                    "document_types": ','.join(document_types) if document_types else None,
                    "threshold": similarity_threshold,
                    "limit": limit
                }
            )
            
            chunks_rows = chunks_result.fetchall()
            
            # Search in knowledge base for general knowledge
            kb_query = text("""
                SELECT 
                    id, title, content, summary, category, subcategory, tags, 
                    source, source_url, confidence_level,
                    1 - (embedding <=> :query_vector) as similarity_score
                FROM knowledge_base 
                WHERE is_active = true
                AND (:contract_category IS NULL OR category = :contract_category)
                AND 1 - (embedding <=> :query_vector) > :threshold
                ORDER BY embedding <=> :query_vector
                LIMIT :kb_limit
            """)
            
            kb_result = await db.execute(
                kb_query,
                {
                    "query_vector": str(query_vector),
                    "contract_category": contract_category,
                    "threshold": similarity_threshold,
                    "kb_limit": min(limit // 2, 5)
                }
            )
            
            kb_rows = kb_result.fetchall()
            
            return {
                "legal_chunks": [
                    {
                        "id": str(row.id),
                        "content": row.content,
                        "chunk_type": row.chunk_type,
                        "section_title": row.section_title,
                        "importance_score": float(row.importance_score or 0),
                        "legal_concepts": row.legal_concepts or [],
                        "document": {
                            "title": row.title,
                            "document_type": row.document_type,
                            "category": row.category,
                            "source": row.source,
                            "reference_number": row.reference_number,
                            "authority_level": row.authority_level,
                            "publication_date": row.publication_date.isoformat() if row.publication_date else None
                        },
                        "similarity_score": float(row.similarity_score)
                    }
                    for row in chunks_rows
                ],
                "knowledge_base": [
                    {
                        "id": str(row.id),
                        "title": row.title,
                        "content": row.content,
                        "summary": row.summary,
                        "category": row.category,
                        "subcategory": row.subcategory,
                        "tags": row.tags or [],
                        "source": row.source,
                        "source_url": row.source_url,
                        "confidence_level": float(row.confidence_level),
                        "similarity_score": float(row.similarity_score)
                    }
                    for row in kb_rows
                ],
                "query_metadata": {
                    "query": query,
                    "contract_category": contract_category,
                    "document_types": document_types,
                    "authority_level": authority_level,
                    "similarity_threshold": similarity_threshold,
                    "total_chunks": len(chunks_rows),
                    "total_kb_entries": len(kb_rows)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in legal knowledge search: {e}")
            raise

    async def search(
        self, 
        query: str, 
        contract_type: Optional[str] = None,
        limit: int = 5,
        similarity_threshold: float = 0.7,
        db: Optional[AsyncSession] = None
    ) -> List[Dict[str, Any]]:
        """
        Legacy search method for backward compatibility
        """
        result = await self.search_legal_knowledge(
            query=query,
            contract_category=contract_type,
            limit=limit,
            similarity_threshold=similarity_threshold,
            db=db
        )
        
        # Combine results for legacy format
        combined_results = []
        
        # Add legal chunks
        for chunk in result["legal_chunks"]:
            combined_results.append({
                "id": chunk["id"],
                "title": chunk["document"]["title"],
                "content": chunk["content"],
                "summary": chunk["section_title"] or chunk["content"][:200] + "...",
                "category": chunk["document"]["category"],
                "subcategory": chunk["document"]["document_type"],
                "source": chunk["document"]["source"],
                "similarity_score": chunk["similarity_score"]
            })
        
        # Add knowledge base entries
        for kb_entry in result["knowledge_base"]:
            combined_results.append(kb_entry)
        
        # Sort by similarity score and return top results
        combined_results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return combined_results[:limit]
        
        rows = result.fetchall()
        
        # Format results
        results = []
        for row in rows:
            results.append({
                "id": str(row.id),
                "title": row.title,
                "content": row.content,
                "summary": row.summary,
                "category": row.category,
                "subcategory": row.subcategory,
                "tags": row.tags,
                "source": row.source,
                "source_url": row.source_url,
                "confidence_level": row.confidence_level,
                "similarity_score": float(row.similarity_score)
            })
        
        return results
    
    async def add_knowledge(
        self,
        title: str,
        content: str,
        category: str,
        summary: Optional[str] = None,
        subcategory: Optional[str] = None,
        tags: Optional[List[str]] = None,
        source: Optional[str] = None,
        source_url: Optional[str] = None,
        confidence_level: float = 1.0,
        db: Optional[AsyncSession] = None
    ) -> str:
        """
        Add new knowledge to the knowledge base with vector embedding
        
        Returns:
            ID of the created knowledge entry
        """
        if not db:
            raise ValueError("Database session is required")
        
        # Generate embedding for the content
        embeddings = await self.create_embeddings([content])
        embedding_vector = embeddings[0]
        
        # Create knowledge base entry
        kb_entry = KnowledgeBase(
            title=title,
            content=content,
            summary=summary or content[:200] + "...",
            category=category,
            subcategory=subcategory,
            tags=tags or [],
            source=source,
            source_url=source_url,
            confidence_level=confidence_level,
            embedding=embedding_vector
        )
        
        db.add(kb_entry)
        await db.commit()
        await db.refresh(kb_entry)
        
        return str(kb_entry.id)
    
    async def index_legal_document(
        self,
        title: str,
        content: str,
        document_type: str,
        category: str,
        source: str,
        reference_number: Optional[str] = None,
        authority_level: str = "medium",
        legal_area: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        db: Optional[AsyncSession] = None
    ) -> str:
        """
        Index a legal document by creating chunks and embeddings
        
        Args:
            title: Document title
            content: Full document content
            document_type: Type (lei, jurisprudencia, doutrina, etc.)
            category: Contract category (locacao, telecom, financeiro, etc.)
            source: Source of the document (STF, STJ, etc.)
            reference_number: Law number, process number, etc.
            authority_level: Authority level (high, medium, low)
            legal_area: Areas of law this document covers
            keywords: Keywords for the document
            chunk_size: Maximum size of each chunk
            chunk_overlap: Overlap between chunks
            db: Database session
            
        Returns:
            ID of the created legal document
        """
        if not db:
            raise ValueError("Database session is required")
        
        try:
            # Create legal document record
            legal_doc = LegalDocument(
                title=title,
                document_type=document_type,
                category=category,
                content=content,
                source=source,
                reference_number=reference_number,
                authority_level=authority_level,
                legal_area=legal_area or [],
                keywords=keywords or [],
                processing_status="processing"
            )
            
            db.add(legal_doc)
            await db.flush()  # Get the ID without committing
            
            # Create chunks
            chunks = self._create_text_chunks(content, chunk_size, chunk_overlap)
            
            # Generate embeddings for all chunks
            chunk_texts = [chunk["text"] for chunk in chunks]
            embeddings = await self.create_embeddings(chunk_texts)
            
            # Create chunk records
            chunk_objects = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_obj = LegalChunk(
                    document_id=legal_doc.id,
                    content=chunk["text"],
                    chunk_type="text",
                    chunk_order=i,
                    start_position=chunk.get("start", 0),
                    end_position=chunk.get("end", len(chunk["text"])),
                    embedding=embedding,
                    word_count=len(chunk["text"].split()),
                    char_count=len(chunk["text"]),
                    importance_score=self._calculate_importance_score(chunk["text"])
                )
                chunk_objects.append(chunk_obj)
            
            db.add_all(chunk_objects)
            
            # Update document status
            legal_doc.processing_status = "indexed"
            legal_doc.chunk_count = len(chunk_objects)
            legal_doc.indexed_at = asyncio.get_event_loop().time()
            
            await db.commit()
            await db.refresh(legal_doc)
            
            logger.info(f"Indexed legal document {title} with {len(chunk_objects)} chunks")
            return str(legal_doc.id)
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Error indexing legal document: {e}")
            raise
    
    def _create_text_chunks(
        self, 
        text: str, 
        chunk_size: int = 1000, 
        chunk_overlap: int = 200
    ) -> List[Dict[str, Any]]:
        """Create overlapping text chunks from a document"""
        
        # Split by paragraphs first to maintain context
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        chunks = []
        current_chunk = ""
        current_start = 0
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size
            if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
                chunks.append({
                    "text": current_chunk.strip(),
                    "start": current_start,
                    "end": current_start + len(current_chunk)
                })
                
                # Create overlapping chunk
                overlap_text = current_chunk[-chunk_overlap:] if len(current_chunk) > chunk_overlap else current_chunk
                current_chunk = overlap_text + " " + paragraph
                current_start = current_start + len(current_chunk) - len(overlap_text) - len(paragraph) - 1
            else:
                if current_chunk:
                    current_chunk += " " + paragraph
                else:
                    current_chunk = paragraph
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                "text": current_chunk.strip(),
                "start": current_start,
                "end": current_start + len(current_chunk)
            })
        
        return chunks
    
    def _calculate_importance_score(self, text: str) -> float:
        """Calculate importance score based on text characteristics"""
        
        # Simple heuristic based on legal terms and structure
        legal_terms = [
            "artigo", "lei", "código", "constituição", "decreto", 
            "jurisprudência", "súmula", "acórdão", "decisão",
            "contrato", "cláusula", "direito", "dever", "obrigação"
        ]
        
        text_lower = text.lower()
        score = 1.0
        
        # Boost for legal terms
        for term in legal_terms:
            if term in text_lower:
                score += 0.1
        
        # Boost for structured text (articles, sections)
        if any(pattern in text_lower for pattern in ["art.", "§", "inciso", "alínea"]):
            score += 0.2
        
        # Boost for citations
        if any(pattern in text for pattern in ["Lei", "Código", "CF/88"]):
            score += 0.15
        
        return min(score, 2.0)  # Cap at 2.0
    
    async def update_knowledge(
        self,
        knowledge_id: str,
        content: Optional[str] = None,
        title: Optional[str] = None,
        summary: Optional[str] = None,
        db: Optional[AsyncSession] = None
    ) -> bool:
        """Update existing knowledge and regenerate embedding if content changed"""
        if not db:
            raise ValueError("Database session is required")
        
        # Get existing entry
        result = await db.execute(
            select(KnowledgeBase).where(KnowledgeBase.id == knowledge_id)
        )
        kb_entry = result.scalar_one_or_none()
        
        if not kb_entry:
            return False
        
        # Update fields
        if title:
            kb_entry.title = title
        if summary:
            kb_entry.summary = summary
        
        # If content changed, regenerate embedding
        if content and content != kb_entry.content:
            kb_entry.content = content
            embeddings = await self.create_embeddings([content])
            kb_entry.embedding = embeddings[0]
        
        await db.commit()
        return True
    
    async def get_knowledge_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        
        # Total count
        total_result = await db.execute(
            select(KnowledgeBase).where(KnowledgeBase.is_active == True)
        )
        total_count = len(total_result.scalars().all())
        
        # Count by category
        category_result = await db.execute(
            text("""
                SELECT category, COUNT(*) as count 
                FROM knowledge_base 
                WHERE is_active = true 
                GROUP BY category
            """)
        )
        
        categories = {}
        for row in category_result.fetchall():
            categories[row.category] = row.count
        
        return {
            "total_entries": total_count,
            "categories": categories,
            "embedding_dimension": self.embedding_dimension
        }
    
    async def build_context_for_agent(
        self,
        query: str,
        contract_type: str,
        context_type: str = "analysis",
        max_context_length: int = 4000,
        db: Optional[AsyncSession] = None
    ) -> Dict[str, Any]:
        """
        Build enriched context for AI agents based on query and contract type
        
        Args:
            query: The user query or contract analysis request
            contract_type: Type of contract (locacao, telecom, financeiro)
            context_type: Type of context needed (analysis, risk_assessment, clause_review)
            max_context_length: Maximum length of context text
            db: Database session
            
        Returns:
            Structured context with legal knowledge, precedents, and guidelines
        """
        if not db:
            raise ValueError("Database session is required")
        
        try:
            # Search for relevant legal knowledge
            legal_results = await self.search_legal_knowledge(
                query=query,
                contract_category=contract_type,
                document_types=["lei", "jurisprudencia", "doutrina"],
                limit=8,
                similarity_threshold=0.7,
                db=db
            )
            
            # Build structured context
            context = {
                "contract_type": contract_type,
                "query": query,
                "context_type": context_type,
                "legal_framework": [],
                "jurisprudence": [],
                "risk_indicators": [],
                "recommendations": [],
                "raw_context": ""
            }
            
            current_length = 0
            
            # Process legal chunks by type
            for chunk in legal_results["legal_chunks"]:
                if current_length >= max_context_length:
                    break
                
                doc_type = chunk["document"]["document_type"]
                content_snippet = chunk["content"][:300] + "..." if len(chunk["content"]) > 300 else chunk["content"]
                
                chunk_info = {
                    "content": content_snippet,
                    "source": chunk["document"]["source"],
                    "reference": chunk["document"]["reference_number"],
                    "authority_level": chunk["document"]["authority_level"],
                    "similarity_score": chunk["similarity_score"]
                }
                
                if doc_type in ["lei", "decreto", "código"]:
                    context["legal_framework"].append(chunk_info)
                elif doc_type == "jurisprudencia":
                    context["jurisprudence"].append(chunk_info)
                
                # Add to raw context for LLM
                context["raw_context"] += f"\n\n[{doc_type.upper()} - {chunk['document']['source']}]\n{content_snippet}\n"
                current_length += len(content_snippet)
            
            # Add knowledge base insights
            for kb_entry in legal_results["knowledge_base"]:
                if current_length >= max_context_length:
                    break
                
                if kb_entry["category"] == contract_type:
                    content_snippet = kb_entry["content"][:200] + "..." if len(kb_entry["content"]) > 200 else kb_entry["content"]
                    
                    context["recommendations"].append({
                        "title": kb_entry["title"],
                        "content": content_snippet,
                        "confidence": kb_entry["confidence_level"],
                        "similarity_score": kb_entry["similarity_score"]
                    })
                    
                    context["raw_context"] += f"\n\n[GUIDELINE - {kb_entry['title']}]\n{content_snippet}\n"
                    current_length += len(content_snippet)
            
            # Trim raw context if too long
            if len(context["raw_context"]) > max_context_length:
                context["raw_context"] = context["raw_context"][:max_context_length] + "..."
            
            # Add context metadata
            context["metadata"] = {
                "total_sources": len(legal_results["legal_chunks"]) + len(legal_results["knowledge_base"]),
                "context_length": len(context["raw_context"]),
                "high_authority_sources": len([
                    c for c in legal_results["legal_chunks"] 
                    if c["document"]["authority_level"] == "high"
                ]),
                "generated_at": asyncio.get_event_loop().time()
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Error building context for agent: {e}")
            raise
    
    async def get_legal_precedents(
        self,
        contract_clause: str,
        contract_type: str,
        limit: int = 5,
        db: Optional[AsyncSession] = None
    ) -> List[Dict[str, Any]]:
        """
        Get legal precedents specifically related to a contract clause
        """
        precedents_query = f"jurisprudência {contract_clause} {contract_type}"
        
        results = await self.search_legal_knowledge(
            query=precedents_query,
            contract_category=contract_type,
            document_types=["jurisprudencia"],
            authority_level="high",
            limit=limit,
            similarity_threshold=0.8,
            db=db
        )
        
        return [
            {
                "court": chunk["document"]["source"],
                "case_reference": chunk["document"]["reference_number"],
                "content": chunk["content"],
                "relevance_score": chunk["similarity_score"],
                "authority_level": chunk["document"]["authority_level"]
            }
            for chunk in results["legal_chunks"]
        ]

# Global RAG service instance (lazy initialization)
rag_service = None

def get_rag_service() -> RAGService:
    """Get or create the global RAG service instance"""
    global rag_service
    if rag_service is None:
        rag_service = RAGService()
    return rag_service
