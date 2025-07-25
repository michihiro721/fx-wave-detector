"""Initial database setup

Revision ID: 001
Revises: 
Create Date: 2025-07-13 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('line_user_id', sa.String(length=100), nullable=False),
    sa.Column('display_name', sa.String(length=255), nullable=True),
    sa.Column('picture_url', sa.Text(), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('line_notifications_enabled', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_line_user_id'), 'users', ['line_user_id'], unique=True)
    
    op.create_table('fx_prices',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('pair', sa.String(length=10), nullable=False),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('open_price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('high_price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('low_price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('close_price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('volume', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fx_prices_pair'), 'fx_prices', ['pair'], unique=False)
    op.create_index(op.f('ix_fx_prices_timestamp'), 'fx_prices', ['timestamp'], unique=False)
    
    op.create_table('daily_price_summaries',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('pair', sa.String(length=10), nullable=False),
    sa.Column('date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('open_price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('high_price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('low_price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('close_price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('volume', sa.BigInteger(), nullable=True),
    sa.Column('volatility', sa.Numeric(precision=8, scale=5), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_daily_price_summaries_pair'), 'daily_price_summaries', ['pair'], unique=False)
    op.create_index(op.f('ix_daily_price_summaries_date'), 'daily_price_summaries', ['date'], unique=False)
    
    op.create_table('wave_alerts',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('pair', sa.String(length=10), nullable=False),
    sa.Column('wave_type', sa.Integer(), nullable=False),
    sa.Column('price', sa.Numeric(precision=10, scale=5), nullable=True),
    sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
    sa.Column('sent_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wave_alerts_user_id'), 'wave_alerts', ['user_id'], unique=False)
    op.create_index(op.f('ix_wave_alerts_pair'), 'wave_alerts', ['pair'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wave_alerts_pair'), table_name='wave_alerts')
    op.drop_index(op.f('ix_wave_alerts_user_id'), table_name='wave_alerts')
    op.drop_table('wave_alerts')
    op.drop_index(op.f('ix_daily_price_summaries_date'), table_name='daily_price_summaries')
    op.drop_index(op.f('ix_daily_price_summaries_pair'), table_name='daily_price_summaries')
    op.drop_table('daily_price_summaries')
    op.drop_index(op.f('ix_fx_prices_timestamp'), table_name='fx_prices')
    op.drop_index(op.f('ix_fx_prices_pair'), table_name='fx_prices')
    op.drop_table('fx_prices')
    op.drop_index(op.f('ix_users_line_user_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###