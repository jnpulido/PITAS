"""new version

Revision ID: 0e818580973c
Revises: 5356a8879dbe
Create Date: 2026-03-20 15:07:54.380563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0e818580973c'
down_revision: Union[str, Sequence[str], None] = '5356a8879dbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


movement_type_enum = sa.Enum(
    'IN',
    'OUT',
    'ADJUSTMENT',
    name='movement_type'
)


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()

    # Crear el tipo enum en PostgreSQL si no existe
    movement_type_enum.create(bind, checkfirst=True)

    # Agregar la nueva columna como nullable temporalmente
    op.add_column(
        'ingredients_stock_moviments',
        sa.Column('type_movement', movement_type_enum, nullable=True)
    )

    # Migrar datos desde la columna vieja string a la nueva enum
    op.execute("""
        UPDATE ingredients_stock_moviments
        SET type_movement = CASE
            WHEN UPPER(type_moviment) IN ('IN', 'INPUT', 'ENTRADA') THEN 'IN'::movement_type
            WHEN UPPER(type_moviment) IN ('OUT', 'OUTPUT', 'SALIDA') THEN 'OUT'::movement_type
            WHEN UPPER(type_moviment) IN ('ADJUSTMENT', 'AJUSTE') THEN 'ADJUSTMENT'::movement_type
            ELSE 'ADJUSTMENT'::movement_type
        END
    """)

    # Hacer la columna obligatoria una vez cargados los datos
    op.alter_column(
        'ingredients_stock_moviments',
        'type_movement',
        nullable=False
    )

    # Eliminar la columna vieja
    op.drop_column('ingredients_stock_moviments', 'type_moviment')


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()

    # Recrear la columna vieja
    op.add_column(
        'ingredients_stock_moviments',
        sa.Column('type_moviment', sa.String(length=120), nullable=True)
    )

    # Pasar datos desde enum a string
    op.execute("""
        UPDATE ingredients_stock_moviments
        SET type_moviment = type_movement::text
    """)

    # Dejarla obligatoria
    op.alter_column(
        'ingredients_stock_moviments',
        'type_moviment',
        nullable=False
    )

    # Borrar la columna enum
    op.drop_column('ingredients_stock_moviments', 'type_movement')

    # Borrar el tipo enum de PostgreSQL
    movement_type_enum.drop(bind, checkfirst=True)