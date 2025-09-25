"""Create vector indexes for RAG tables

Revision ID: 002_rag_vector_indexes
Revises: 001_enable_pgvector
Create Date: 2024-01-20 10:30:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '002_rag_vector_indexes'
down_revision = '001_enable_pgvector'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create vector indexes for legal_chunks table
    # Using IVFFlat index for better performance with cosine similarity
    op.execute('''
        CREATE INDEX IF NOT EXISTS legal_chunks_embedding_idx 
        ON legal_chunks USING ivfflat (embedding vector_cosine_ops) 
        WITH (lists = 100)
    ''')
    
    # Create composite indexes for better query performance
    op.execute('''
        CREATE INDEX IF NOT EXISTS legal_chunks_document_category_idx 
        ON legal_chunks (document_id) 
        INCLUDE (chunk_type, chunk_order)
    ''')
    
    op.execute('''
        CREATE INDEX IF NOT EXISTS legal_documents_category_type_idx 
        ON legal_documents (category, document_type, is_active)
    ''')
    
    op.execute('''
        CREATE INDEX IF NOT EXISTS legal_documents_processing_status_idx 
        ON legal_documents (processing_status, indexed_at)
    ''')


def downgrade() -> None:
    # Drop vector indexes
    op.execute('DROP INDEX IF EXISTS legal_chunks_embedding_idx')
    op.execute('DROP INDEX IF EXISTS legal_chunks_document_category_idx')
    op.execute('DROP INDEX IF EXISTS legal_documents_category_type_idx')
    op.execute('DROP INDEX IF EXISTS legal_documents_processing_status_idx')