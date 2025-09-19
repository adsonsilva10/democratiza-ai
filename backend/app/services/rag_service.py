from typing import List, Dict, Any, Optional
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from sentence_transformers import SentenceTransformer
import numpy as np
from app.db.models import KnowledgeBase
from app.core.config import settings

class RAGService:
    """Retrieval-Augmented Generation service for legal knowledge"""
    
    def __init__(self):
        self.embedding_model = None
        self._model_loading = False
    
    async def initialize(self):
        """Initialize the embedding model (lazy loading)"""
        if self.embedding_model is None and not self._model_loading:
            self._model_loading = True
            # Load sentence transformer model in a separate thread
            loop = asyncio.get_event_loop()
            self.embedding_model = await loop.run_in_executor(
                None, 
                lambda: SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            )
            self._model_loading = False
    
    async def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Create embeddings for a list of texts"""
        await self.initialize()
        
        # Generate embeddings in a separate thread to avoid blocking
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None,
            lambda: self.embedding_model.encode(texts).tolist()
        )
        return embeddings
    
    async def search(
        self, 
        query: str, 
        contract_type: Optional[str] = None,
        limit: int = 5,
        similarity_threshold: float = 0.7,
        db: Optional[AsyncSession] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for relevant knowledge base entries using vector similarity
        
        Args:
            query: Search query text
            contract_type: Filter by contract type (locacao, telecom, financeiro, etc.)
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score
            db: Database session
            
        Returns:
            List of relevant knowledge base entries with similarity scores
        """
        if not db:
            raise ValueError("Database session is required")
        
        # Generate query embedding
        query_embeddings = await self.create_embeddings([query])
        query_vector = query_embeddings[0]
        
        # Build base query
        base_query = select(KnowledgeBase).where(KnowledgeBase.is_active == True)
        
        # Filter by contract type if specified
        if contract_type:
            base_query = base_query.where(KnowledgeBase.category == contract_type)
        
        # Execute vector similarity search using pgvector
        # Note: This requires the pgvector extension and proper vector column
        similarity_query = text("""
            SELECT 
                id, title, content, summary, category, subcategory, tags, 
                source, source_url, confidence_level,
                1 - (embedding <=> :query_vector) as similarity_score
            FROM knowledge_base 
            WHERE is_active = true
            AND (:contract_type IS NULL OR category = :contract_type)
            AND 1 - (embedding <=> :query_vector) > :threshold
            ORDER BY embedding <=> :query_vector
            LIMIT :limit
        """)
        
        result = await db.execute(
            similarity_query,
            {
                "query_vector": str(query_vector),
                "contract_type": contract_type,
                "threshold": similarity_threshold,
                "limit": limit
            }
        )
        
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
            "embedding_dimension": settings.EMBEDDING_DIMENSION
        }

# Global RAG service instance
rag_service = RAGService()
