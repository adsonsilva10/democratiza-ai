"""
Democratiza AI - Database Models
Sistema completo de modelos para o banco de dados PostgreSQL/Supabase
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID, ENUM

Base = declarative_base()

# Enum para tipos de contrato
contract_type_enum = ENUM(
    'rental',           # Locação
    'telecom',          # Telecomunicações
    'financial',        # Financeiro/Bancário
    'insurance',        # Seguros
    'employment',       # Trabalhista
    'service',          # Prestação de Serviços
    'purchase',         # Compra e Venda
    'partnership',      # Sociedade/Parceria
    'other',           # Outros
    name='contract_type'
)

# Enum para status de análise
analysis_status_enum = ENUM(
    'pending',         # Pendente
    'processing',      # Processando
    'completed',       # Concluído
    'failed',          # Falha
    'cancelled',       # Cancelado
    name='analysis_status'
)

# Enum para nível de risco
risk_level_enum = ENUM(
    'low',            # Baixo risco
    'medium',         # Médio risco
    'high',           # Alto risco
    'critical',       # Crítico
    name='risk_level'
)


class User(Base):
    """Modelo de usuário integrado com Supabase Auth"""
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    supabase_user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    
    # Informações básicas
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    avatar_url = Column(String(500))
    
    # Configurações do usuário
    subscription_plan = Column(String(50), default='free')  # free, basic, premium
    credits_remaining = Column(Integer, default=3)  # Créditos para análises
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True))
    
    # Relacionamentos
    contracts = relationship("Contract", back_populates="user")
    analyses = relationship("ContractAnalysis", back_populates="user")
    configurations = relationship("UserConfiguration", back_populates="user")


class Contract(Base):
    """Modelo para contratos enviados pelos usuários"""
    __tablename__ = 'contracts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Informações do arquivo
    original_filename = Column(String(500), nullable=False)
    file_path = Column(String(1000))  # Path no Supabase Storage
    file_size = Column(Integer)  # Tamanho em bytes
    mime_type = Column(String(100))
    
    # Conteúdo extraído
    raw_text = Column(Text)  # Texto extraído via OCR
    processed_text = Column(Text)  # Texto processado e limpo
    
    # Classificação automática
    contract_type = Column(contract_type_enum, index=True)
    confidence_score = Column(Float)  # Confiança na classificação (0-1)
    
    # Metadados
    page_count = Column(Integer)
    word_count = Column(Integer)
    
    # Status
    is_processed = Column(Boolean, default=False)
    processing_started_at = Column(DateTime(timezone=True))
    processing_completed_at = Column(DateTime(timezone=True))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="contracts")
    analyses = relationship("ContractAnalysis", back_populates="contract")


class ContractAnalysis(Base):
    """Análises de contratos geradas pela IA"""
    __tablename__ = 'contract_analyses'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contracts.id'), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Status da análise
    status = Column(analysis_status_enum, default='pending', index=True)
    
    # Resultado da análise
    overall_risk_level = Column(risk_level_enum, index=True)
    risk_score = Column(Float)  # Score numérico (0-100)
    
    # Análise detalhada (JSON estruturado)
    analysis_data = Column(JSON)  # Resultado completo da análise
    """
    Estrutura do analysis_data:
    {
        "summary": "Resumo executivo da análise",
        "key_terms": ["Termo 1", "Termo 2"],
        "risk_factors": [
            {
                "category": "payment_terms",
                "risk_level": "high",
                "description": "Descrição do risco",
                "suggestion": "Sugestão de melhoria"
            }
        ],
        "positive_aspects": ["Aspecto positivo 1"],
        "recommendations": ["Recomendação 1"],
        "legal_references": ["Artigo X do CDC"],
        "alerts": ["Alerta importante"]
    }
    """
    
    # Cláusulas específicas analisadas
    clauses_analysis = Column(JSON)
    """
    Estrutura das cláusulas:
    {
        "abusive_clauses": [
            {
                "text": "Texto da cláusula",
                "reason": "Motivo da classificação",
                "article": "Artigo legal aplicável"
            }
        ],
        "payment_terms": {...},
        "termination_conditions": {...},
        "warranties": {...}
    }
    """
    
    # IA Agent utilizado
    agent_used = Column(String(100))  # rental_agent, financial_agent, etc.
    model_version = Column(String(50))  # Versão do modelo Claude usado
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relacionamentos
    contract = relationship("Contract", back_populates="analyses")
    user = relationship("User", back_populates="analyses")
    chat_sessions = relationship("ChatSession", back_populates="analysis")


class ChatSession(Base):
    """Sessões de chat sobre contratos específicos"""
    __tablename__ = 'chat_sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey('contract_analyses.id'), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Configurações da sessão
    title = Column(String(500))  # Título gerado automaticamente
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_message_at = Column(DateTime(timezone=True))
    
    # Relacionamentos
    analysis = relationship("ContractAnalysis", back_populates="chat_sessions")
    user = relationship("User")
    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    """Mensagens individuais do chat"""
    __tablename__ = 'chat_messages'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey('chat_sessions.id'), nullable=False, index=True)
    
    # Conteúdo da mensagem
    content = Column(Text, nullable=False)
    role = Column(String(20), nullable=False)  # 'user' ou 'assistant'
    
    # Metadados
    tokens_used = Column(Integer)  # Tokens consumidos (para billing)
    model_used = Column(String(100))  # Modelo específico usado
    response_time_ms = Column(Integer)  # Tempo de resposta em ms
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    session = relationship("ChatSession", back_populates="messages")


class UserConfiguration(Base):
    """Configurações personalizadas do usuário"""
    __tablename__ = 'user_configurations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False, index=True)
    
    # Preferências de análise
    preferred_risk_sensitivity = Column(String(20), default='medium')  # low, medium, high
    notification_preferences = Column(JSON, default={})
    theme_preference = Column(String(20), default='light')  # light, dark, auto
    
    # Configurações de privacidade
    allow_data_usage_analytics = Column(Boolean, default=True)
    allow_improvement_suggestions = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    user = relationship("User", back_populates="configurations")


class DocumentVector(Base):
    """Vetores para RAG (Retrieval Augmented Generation)"""
    __tablename__ = 'document_vectors'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    contract_id = Column(UUID(as_uuid=True), ForeignKey('contracts.id'), nullable=False, index=True)
    
    # Conteúdo e embedding
    text_chunk = Column(Text, nullable=False)  # Pedaço do texto
    chunk_index = Column(Integer, nullable=False)  # Índice do chunk no documento
    
    # Embedding será armazenado usando pg_vector
    # embedding = Column(Vector(1536))  # Será configurado após habilitar pg_vector
    
    # Metadados
    chunk_tokens = Column(Integer)  # Quantidade de tokens no chunk
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    contract = relationship("Contract")


class AuditLog(Base):
    """Log de auditoria para rastreabilidade"""
    __tablename__ = 'audit_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), index=True)
    
    # Ação realizada
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False)  # contract, analysis, user
    resource_id = Column(UUID(as_uuid=True))
    
    # Detalhes da ação
    details = Column(JSON)
    ip_address = Column(String(45))  # IPv4 ou IPv6
    user_agent = Column(String(500))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relacionamentos
    user = relationship("User")