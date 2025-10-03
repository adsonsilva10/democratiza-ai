"""Add storage audit log table

Revision ID: add_storage_audit_log
Revises: 
Create Date: 2025-10-03 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSON


# revision identifiers, used by Alembic.
revision: str = 'add_storage_audit_log'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add storage_audit_logs table."""
    op.create_table('storage_audit_logs',
        sa.Column('id', UUID(as_uuid=True), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', UUID(as_uuid=True), nullable=False),
        sa.Column('operation', sa.String(), nullable=False),
        sa.Column('file_id', sa.String(), nullable=False),
        sa.Column('file_name', sa.String(), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=True),
        sa.Column('ip_address', sa.String(), nullable=True),
        sa.Column('user_agent', sa.String(), nullable=True),
        sa.Column('success', sa.Boolean(), nullable=False),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('operation_metadata', JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_storage_audit_logs_user_id'), 'storage_audit_logs', ['user_id'], unique=False)
    op.create_index(op.f('ix_storage_audit_logs_file_id'), 'storage_audit_logs', ['file_id'], unique=False)
    op.create_index(op.f('ix_storage_audit_logs_operation'), 'storage_audit_logs', ['operation'], unique=False)
    op.create_index(op.f('ix_storage_audit_logs_created_at'), 'storage_audit_logs', ['created_at'], unique=False)


def downgrade() -> None:
    """Remove storage_audit_logs table."""
    op.drop_index(op.f('ix_storage_audit_logs_created_at'), table_name='storage_audit_logs')
    op.drop_index(op.f('ix_storage_audit_logs_operation'), table_name='storage_audit_logs')
    op.drop_index(op.f('ix_storage_audit_logs_file_id'), table_name='storage_audit_logs')
    op.drop_index(op.f('ix_storage_audit_logs_user_id'), table_name='storage_audit_logs')
    op.drop_table('storage_audit_logs')