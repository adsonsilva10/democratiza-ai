"""Add AI columns to contracts table

Revision ID: 002_add_ai_columns
Revises: 001_initial
Create Date: 2025-10-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = '002_add_ai_columns'
down_revision = None  # Start fresh since alembic_version is empty
branch_labels = None
depends_on = None


def upgrade():
    """Add AI and analysis columns to contracts table"""
    
    # Check if columns already exist before adding
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    existing_columns = [col['name'] for col in inspector.get_columns('contracts')]
    
    # Add text_embedding column (OpenAI 1536 dimensions)
    if 'text_embedding' not in existing_columns:
        op.add_column('contracts', 
            sa.Column('text_embedding', Vector(1536), nullable=True)
        )
        print("✅ Added text_embedding column (Vector 1536)")
    
    # Add LLM metadata columns
    if 'llm_model_used' not in existing_columns:
        op.add_column('contracts',
            sa.Column('llm_model_used', sa.String(), nullable=True)
        )
    
    if 'llm_provider_used' not in existing_columns:
        op.add_column('contracts',
            sa.Column('llm_provider_used', sa.String(), nullable=True)
        )
    
    if 'complexity_level' not in existing_columns:
        op.add_column('contracts',
            sa.Column('complexity_level', sa.String(), nullable=True)
        )
    
    if 'analysis_cost_usd' not in existing_columns:
        op.add_column('contracts',
            sa.Column('analysis_cost_usd', sa.Numeric(10, 6), nullable=True)
        )
    
    # Add analysis result columns
    if 'abusive_clauses' not in existing_columns:
        op.add_column('contracts',
            sa.Column('abusive_clauses', postgresql.JSONB(), nullable=True)
        )
    
    if 'payment_terms' not in existing_columns:
        op.add_column('contracts',
            sa.Column('payment_terms', postgresql.JSONB(), nullable=True)
        )
    
    if 'termination_conditions' not in existing_columns:
        op.add_column('contracts',
            sa.Column('termination_conditions', postgresql.JSONB(), nullable=True)
        )
    
    if 'analysis_result' not in existing_columns:
        op.add_column('contracts',
            sa.Column('analysis_result', postgresql.JSONB(), nullable=True)
        )
    
    print("✅ Added LLM and analysis columns")
    
    # Create vector similarity index
    try:
        op.execute("""
            CREATE INDEX IF NOT EXISTS idx_contracts_embedding 
            ON contracts USING ivfflat (text_embedding vector_cosine_ops)
            WITH (lists = 100)
        """)
        print("✅ Created ivfflat index for vector similarity search")
    except Exception as e:
        print(f"⚠️  Index creation skipped (may already exist): {e}")


def downgrade():
    """Remove AI columns from contracts table"""
    
    # Drop index
    op.execute("DROP INDEX IF EXISTS idx_contracts_embedding")
    
    # Drop columns
    op.drop_column('contracts', 'analysis_result')
    op.drop_column('contracts', 'termination_conditions')
    op.drop_column('contracts', 'payment_terms')
    op.drop_column('contracts', 'abusive_clauses')
    op.drop_column('contracts', 'analysis_cost_usd')
    op.drop_column('contracts', 'complexity_level')
    op.drop_column('contracts', 'llm_provider_used')
    op.drop_column('contracts', 'llm_model_used')
    op.drop_column('contracts', 'text_embedding')
