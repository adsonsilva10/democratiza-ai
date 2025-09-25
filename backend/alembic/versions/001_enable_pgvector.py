"""Enable pgvector extension and create vector indexes

Revision ID: 001_enable_pgvector
Revises: 
Create Date: 2024-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision = '001_enable_pgvector'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable pgvector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Create vector indexes for existing knowledge_base table
    op.execute('CREATE INDEX IF NOT EXISTS knowledge_base_embedding_idx ON knowledge_base USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100)')
    
    # Create vector indexes for new legal_chunks table (will be created by models)
    # This will be applied after the new tables are created
    pass


def downgrade() -> None:
    # Drop vector indexes
    op.execute('DROP INDEX IF EXISTS knowledge_base_embedding_idx')
    
    # Note: We don't drop the pgvector extension as it might be used by other applications
    # op.execute('DROP EXTENSION IF EXISTS vector')