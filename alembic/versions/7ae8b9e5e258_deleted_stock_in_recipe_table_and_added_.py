"""deleted stock in recipe table and added unit in recipeIngredient table 

Revision ID: 7ae8b9e5e258
Revises: 87db27dd0549
Create Date: 2026-03-27 17:51:13.062784

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ae8b9e5e258'
down_revision: Union[str, Sequence[str], None] = '87db27dd0549'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""deleted stock in recipe table and added unit in recipeIngredient table

Revision ID: 7ae8b9e5e258
Revises: 87db27dd0549
Create Date: 2026-03-27 17:51:13.062784
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ae8b9e5e258'
down_revision: Union[str, Sequence[str], None] = '87db27dd0549'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


"""deleted stock in recipe table and added unit in recipe_ingredients table

Revision ID: 7ae8b9e5e258
Revises: 87db27dd0549
Create Date: 2026-03-27 17:51:13.062784
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7ae8b9e5e258"
down_revision: Union[str, Sequence[str], None] = "87db27dd0549"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("ingredients", "stock")

    op.add_column(
        "recipe_ingredients",
        sa.Column("unit", sa.Integer(), nullable=False, server_default="1"),
    )

    op.alter_column("recipe_ingredients", "unit", server_default=None)


def downgrade() -> None:
    op.drop_column("recipe_ingredients", "unit")

    op.add_column(
        "ingredients",
        sa.Column("stock", sa.Integer(), nullable=True),
    )