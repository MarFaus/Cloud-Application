"""add stored objects

Revision ID: 001_add_stored_objects
Revises:
Create Date: 2026-10-13

"""
from alembic import op
import sqlalchemy as sa

revision = '001_add_stored_objects'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'stored_objects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original_name', sa.String(length=255), nullable=False),
        sa.Column('storage_name', sa.String(length=255), nullable=False),
        sa.Column('content_type', sa.String(length=100), nullable=True),
        sa.Column('size_bytes', sa.BigInteger(), nullable=False),
        sa.Column('storage_path', sa.String(length=500), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('storage_name', name='uq_stored_objects_storage_name')
    )

def downgrade() -> None:
    op.drop_table('stored_objects')