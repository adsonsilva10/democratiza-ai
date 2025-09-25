"""
Mock RAG Service para desenvolvimento sem custos de APIs externas
Simula funcionalidades de embeddings e busca com dados pré-definidos
"""
import asyncio
from typing import List, Dict, Any, Optional
import json
import hashlib
from datetime import datetime

class MockRAGService:
    """
    Serviço RAG simulado para desenvolvimento
    Usa dados pré-definidos em vez de APIs externas
    """
    
    def __init__(self):
        self.knowledge_base = self._create_mock_knowledge_base()
        self.documents_storage = {}
        
    def _create_mock_knowledge_base(self) -> List[Dict[str, Any]]:
        """Cria base de conhecimento jurídico simulada"""
        return [
            {
                "id": "lei_8078_cdc",
                "title": "Lei 8.078/90 - Código de Defesa do Consumidor",
                "content": """
                Art. 6º São direitos básicos do consumidor:
                I - a proteção da vida, saúde e segurança contra os riscos provocados por práticas no fornecimento de produtos e serviços considerados perigosos ou nocivos;
                II - a educação e divulgação sobre o consumo adequado dos produtos e serviços;
                III - a informação adequada e clara sobre os diferentes produtos e serviços;
                IV - a proteção contra a publicidade enganosa e abusiva;
                V - a modificação das cláusulas contratuais que estabeleçam prestações desproporcionais;
                VI - a efetiva prevenção e reparação de danos patrimoniais e morais, individuais, coletivos e difusos;
                
                Art. 39. É vedado ao fornecedor de produtos ou serviços:
                I - condicionar o fornecimento de produto ou de serviço ao fornecimento de outro produto ou serviço;
                II - recusar atendimento às demandas dos consumidores;
                III - enviar ou entregar ao consumidor, sem solicitação prévia, qualquer produto;
                IV - prevalecer-se da fraqueza ou ignorância do consumidor;
                V - exigir do consumidor vantagem manifestamente excessiva;
                
                Art. 51. São nulas de pleno direito, entre outras, as cláusulas contratuais relativas ao fornecimento de produtos e serviços que:
                I - impossibilitem, exonerem ou atenuem a responsabilidade do fornecedor;
                II - subtraiam ao consumidor a opção de reembolso da quantia já paga;
                III - transfiram responsabilidades a terceiros;
                IV - estabeleçam obrigações consideradas iníquas, abusivas;
                """,
                "category": "consumer_protection",
                "risk_level": "high",
                "embedding": [0.1, 0.2, 0.3] * 512  # Mock embedding vector
            },
            {
                "id": "lei_8245_locacao",
                "title": "Lei 8.245/91 - Lei do Inquilinato",
                "content": """
                Art. 3º O contrato de locação pode ser ajustado por qualquer prazo, dependendo de acordo entre as partes.
                
                Art. 4º Durante o prazo estipulado para a duração do contrato, não poderá o locador reajustar o aluguel.
                
                Art. 9º A locação também poderá ser contratada mediante fiança, seguro de fiança locatícia ou caução.
                
                Art. 23. O locatário é obrigado a:
                I - servir-se do imóvel para o uso convencionado ou presumido;
                II - conservar, como se seu fosse, o imóvel locado;
                III - pagar pontualmente o aluguel e os encargos da locação;
                IV - levar ao conhecimento do locador o surgimento de qualquer dano ou defeito;
                V - realizar a entrega do imóvel, finda a locação, no estado em que o recebeu;
                
                Art. 47. Quando ajustada verbalmente ou por escrito e como prazo igual ou superior a trinta meses, a locação implica direito de preferência, em igualdade de condições com terceiros.
                """,
                "category": "rental_law",
                "risk_level": "medium", 
                "embedding": [0.4, 0.5, 0.6] * 512
            },
            {
                "id": "lei_9472_telecom",
                "title": "Lei 9.472/97 - Lei Geral de Telecomunicações",
                "content": """
                Art. 3º O usuário de serviços de telecomunicações tem direito:
                I - de acesso aos serviços de telecomunicações;
                II - à liberdade de escolha de sua prestadora de serviço;
                III - de não ser discriminado quanto às condições de acesso e fruição do serviço;
                IV - à informação adequada sobre as condições de prestação dos serviços;
                V - à inviolabilidade e ao sigilo de sua comunicação;
                VI - à qualidade do serviço adequada;
                
                Art. 93. A prestadora de serviço de telecomunicações de interesse coletivo tem o direito de:
                I - explorar o serviço conforme estabelecido em ato da Agência;
                II - receber a contraprestação do serviço adequadamente prestado;
                III - solicitar a modificação dos contratos, observado o disposto na regulamentação.
                
                Parágrafo único. É assegurado à prestadora o direito de suspender o serviço por inadimplemento do usuário.
                """,
                "category": "telecom_law",
                "risk_level": "medium",
                "embedding": [0.7, 0.8, 0.9] * 512
            },
            {
                "id": "lei_10406_civil",
                "title": "Lei 10.406/02 - Código Civil - Contratos",
                "content": """
                Art. 421. A liberdade contratual será exercida nos limites da função social do contrato.
                
                Art. 422. Os contratantes são obrigados a guardar, assim na conclusão do contrato, como em sua execução, os princípios de probidade e boa-fé.
                
                Art. 423. Quando houver no contrato de adesão cláusulas ambíguas ou contraditórias, dever-se-á adotar a interpretação mais favorável ao aderente.
                
                Art. 424. Nos contratos de adesão, são nulas as cláusulas que estipulem a renúncia antecipada do aderente a direito resultante da natureza do negócio.
                
                Art. 478. Nos contratos de execução continuada ou diferida, se a prestação de uma das partes se tornar excessivamente onerosa, com extrema vantagem para a outra, em virtude de acontecimentos extraordinários e imprevisíveis, poderá o devedor pedir a resolução do contrato.
                """,
                "category": "civil_law",
                "risk_level": "high",
                "embedding": [0.2, 0.4, 0.8] * 512
            }
        ]
    
    async def create_embeddings(self, text: str) -> List[float]:
        """Simula criação de embeddings usando hash do texto"""
        # Cria um embedding determinístico baseado no texto
        hash_obj = hashlib.md5(text.encode())
        hash_hex = hash_obj.hexdigest()
        
        # Converte para números pseudo-aleatórios mas determinísticos
        embedding = []
        for i in range(0, len(hash_hex), 2):
            byte_val = int(hash_hex[i:i+2], 16)
            normalized_val = (byte_val / 255.0) * 2 - 1  # Normaliza entre -1 e 1
            embedding.append(normalized_val)
        
        # Preenche até 1536 dimensões (padrão OpenAI)
        while len(embedding) < 1536:
            embedding.extend(embedding[:min(16, 1536 - len(embedding))])
        
        return embedding[:1536]
    
    async def search_similar_content(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Simula busca por similaridade usando keywords"""
        query_lower = query.lower()
        results = []
        
        for doc in self.knowledge_base:
            # Simula pontuação de similaridade baseada em palavras-chave
            content_lower = doc["content"].lower()
            title_lower = doc["title"].lower()
            
            score = 0.0
            query_words = query_lower.split()
            
            for word in query_words:
                if word in content_lower:
                    score += 0.3
                if word in title_lower:
                    score += 0.5
                if word in doc["category"]:
                    score += 0.2
            
            # Adiciona contexto específico para diferentes tipos de contratos
            if "aluguel" in query_lower or "locação" in query_lower:
                if doc["category"] == "rental_law":
                    score += 0.8
            elif "telecom" in query_lower or "internet" in query_lower or "celular" in query_lower:
                if doc["category"] == "telecom_law":
                    score += 0.8
            elif "consumidor" in query_lower or "abusiva" in query_lower:
                if doc["category"] == "consumer_protection":
                    score += 0.8
            elif "contrato" in query_lower and doc["category"] == "civil_law":
                score += 0.6
            
            if score > 0:
                result = doc.copy()
                result["similarity_score"] = score
                results.append(result)
        
        # Ordena por pontuação e limita resultados
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:limit]
    
    async def index_document(self, 
                           content: str, 
                           metadata: Dict[str, Any],
                           chunk_size: int = 1000) -> str:
        """Simula indexação de documento"""
        doc_id = f"doc_{hashlib.md5(content.encode()).hexdigest()[:8]}"
        
        # Simula criação de chunks
        chunks = []
        for i in range(0, len(content), chunk_size):
            chunk_text = content[i:i + chunk_size]
            chunk_embedding = await self.create_embeddings(chunk_text)
            
            chunks.append({
                "text": chunk_text,
                "embedding": chunk_embedding,
                "start_index": i,
                "end_index": min(i + chunk_size, len(content))
            })
        
        # Armazena documento
        self.documents_storage[doc_id] = {
            "content": content,
            "metadata": metadata,
            "chunks": chunks,
            "created_at": datetime.now().isoformat()
        }
        
        print(f"✅ Documento indexado com sucesso: {doc_id}")
        return doc_id
    
    async def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Recupera documento pelo ID"""
        return self.documents_storage.get(doc_id)
    
    async def get_relevant_context(self, query: str, max_tokens: int = 2000) -> str:
        """Busca contexto relevante para uma consulta"""
        similar_docs = await self.search_similar_content(query, limit=3)
        
        context_parts = []
        total_length = 0
        
        for doc in similar_docs:
            # Adiciona título e conteúdo mais relevante
            doc_text = f"**{doc['title']}**\n{doc['content'][:800]}"
            
            if total_length + len(doc_text) < max_tokens:
                context_parts.append(doc_text)
                total_length += len(doc_text)
            else:
                # Adiciona o que couber
                remaining_space = max_tokens - total_length
                if remaining_space > 100:
                    context_parts.append(doc_text[:remaining_space-3] + "...")
                break
        
        return "\n\n---\n\n".join(context_parts)

# Instância global simulada
mock_rag_service = MockRAGService()

# Funções de conveniência para compatibilidade
async def search_legal_knowledge(query: str) -> List[Dict[str, Any]]:
    """Busca conhecimento jurídico relevante"""
    return await mock_rag_service.search_similar_content(query)

async def get_contract_analysis_context(contract_type: str, query: str) -> str:
    """Obtém contexto para análise de contratos"""
    combined_query = f"{contract_type} {query}"
    return await mock_rag_service.get_relevant_context(combined_query)