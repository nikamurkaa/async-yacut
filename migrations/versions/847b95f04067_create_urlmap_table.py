"""Создание таблицы URLMap.

Идентификатор ревизии: 847b95f04067
Предыдущая ревизия отсутствует.
Дата создания: 2026-08-21 20:17:42.609113

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '847b95f04067'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Создать таблицу коротких ссылок и её индексы."""
    op.create_table(
        'url_map',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('original', sa.Text(), nullable=False),
        sa.Column('short', sa.String(length=16), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_url_map_short'),
            ['short'],
            unique=True,
        )
        batch_op.create_index(
            batch_op.f('ix_url_map_timestamp'),
            ['timestamp'],
            unique=False,
        )


def downgrade():
    """Удалить таблицу коротких ссылок и её индексы."""
    with op.batch_alter_table('url_map', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_url_map_timestamp'))
        batch_op.drop_index(batch_op.f('ix_url_map_short'))

    op.drop_table('url_map')
