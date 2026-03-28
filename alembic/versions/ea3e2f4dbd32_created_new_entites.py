"""created new entites

Revision ID: ea3e2f4dbd32
Revises: 7ae8b9e5e258
Create Date: 2026-03-27 22:27:12.927453
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "ea3e2f4dbd32"
down_revision: Union[str, Sequence[str], None] = "7ae8b9e5e258"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


movement_type_enum = postgresql.ENUM(
    "in",
    "out",
    "adjustment",
    name="movement_type",
    create_type=False,
)

movement_type_cost_enum = postgresql.ENUM(
    "raw_material",
    "labor",
    "packaging",
    "transport",
    "utilities",
    "other",
    name="movement_type_cost",
    create_type=False,
)

product_movement_type_enum = postgresql.ENUM(
    "in",
    "out",
    "adjustment",
    name="product_movement_type",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()

    # movement_type ya existe en tu base, por eso NO lo creamos acá.
    movement_type_cost_enum.create(bind, checkfirst=True)
    product_movement_type_enum.create(bind, checkfirst=True)

    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=120), nullable=False),
        sa.Column("address", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_customers_id"), "customers", ["id"], unique=False)

    op.create_table(
        "ingredient_prices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ingredient_id"], ["ingredients.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ingredient_prices_id"), "ingredient_prices", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_ingredient_prices_ingredient_id"),
        "ingredient_prices",
        ["ingredient_id"],
        unique=False,
    )

    op.create_table(
        "ingredient_stock_movements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("type_movement", movement_type_enum, nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("ingredient_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["ingredient_id"], ["ingredients.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ingredient_stock_movements_id"),
        "ingredient_stock_movements",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ingredient_stock_movements_ingredient_id"),
        "ingredient_stock_movements",
        ["ingredient_id"],
        unique=False,
    )

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_orders_customer_id"), "orders", ["customer_id"], unique=False)
    op.create_index(op.f("ix_orders_id"), "orders", ["id"], unique=False)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("recipe_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=True),
        sa.Column("validity", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["recipe_id"], ["recipes.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_products_id"), "products", ["id"], unique=False)
    op.create_index(op.f("ix_products_recipe_id"), "products", ["recipe_id"], unique=True)

    op.create_table(
        "batch_costs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("batch_id", sa.Integer(), nullable=False),
        sa.Column("type_movement", movement_type_cost_enum, nullable=False),
        sa.Column("concept", sa.String(length=120), nullable=False),
        sa.Column("quantity", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(["batch_id"], ["batches.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_batch_costs_id"), "batch_costs", ["id"], unique=False)

    op.create_table(
        "presentations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("unit_quantity", sa.Integer(), nullable=True),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("validity", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_presentations_id"), "presentations", ["id"], unique=False)
    op.create_index(
        op.f("ix_presentations_product_id"), "presentations", ["product_id"], unique=False
    )

    op.create_table(
        "product_stock_movements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("type_movement", product_movement_type_enum, nullable=False),
        sa.Column(
            "date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_product_stock_movements_id"),
        "product_stock_movements",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_product_stock_movements_product_id"),
        "product_stock_movements",
        ["product_id"],
        unique=False,
    )

    op.create_table(
        "order_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("presentation_id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("total", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(["order_id"], ["orders.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["presentation_id"], ["presentations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_details_id"), "order_details", ["id"], unique=False)
    op.create_index(
        op.f("ix_order_details_order_id"), "order_details", ["order_id"], unique=False
    )
    op.create_index(
        op.f("ix_order_details_presentation_id"),
        "order_details",
        ["presentation_id"],
        unique=False,
    )

    op.create_table(
        "presentation_price_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("presentation_id", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            "start_date",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["presentation_id"], ["presentations.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_presentation_price_history_id"),
        "presentation_price_history",
        ["id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_presentation_price_history_presentation_id"),
        "presentation_price_history",
        ["presentation_id"],
        unique=False,
    )

    op.drop_index(
        op.f("ix_ingredients_stock_moviments_id"),
        table_name="ingredients_stock_moviments",
    )
    op.drop_index(
        op.f("ix_ingredients_stock_moviments_ingredient_id"),
        table_name="ingredients_stock_moviments",
    )
    op.drop_table("ingredients_stock_moviments")

    op.drop_index(op.f("ix_ingredients_price_id"), table_name="ingredients_price")
    op.drop_index(
        op.f("ix_ingredients_price_ingredient_id"), table_name="ingredients_price"
    )
    op.drop_table("ingredients_price")

    op.alter_column(
        "recipe_ingredients",
        "unit",
        existing_type=sa.INTEGER(),
        type_=sa.String(length=30),
        existing_nullable=False,
        postgresql_using="unit::varchar",
    )


def downgrade() -> None:
    op.alter_column(
        "recipe_ingredients",
        "unit",
        existing_type=sa.String(length=30),
        type_=sa.INTEGER(),
        existing_nullable=False,
        postgresql_using="unit::integer",
    )

    op.create_table(
        "ingredients_price",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "date",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "price",
            sa.NUMERIC(precision=10, scale=2),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("ingredient_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["ingredient_id"],
            ["ingredients.id"],
            name=op.f("ingredients_price_ingredient_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("ingredients_price_pkey")),
    )
    op.create_index(
        op.f("ix_ingredients_price_ingredient_id"),
        "ingredients_price",
        ["ingredient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ingredients_price_id"), "ingredients_price", ["id"], unique=False
    )

    op.create_table(
        "ingredients_stock_moviments",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "date",
            postgresql.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("quantity", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("ingredient_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            "type_movement",
            postgresql.ENUM(
                "in",
                "out",
                "adjustment",
                name="movement_type",
                create_type=False,
            ),
            autoincrement=False,
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["ingredient_id"],
            ["ingredients.id"],
            name=op.f("ingredients_stock_moviments_ingredient_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("ingredients_stock_moviments_pkey")),
    )
    op.create_index(
        op.f("ix_ingredients_stock_moviments_ingredient_id"),
        "ingredients_stock_moviments",
        ["ingredient_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_ingredients_stock_moviments_id"),
        "ingredients_stock_moviments",
        ["id"],
        unique=False,
    )

    op.drop_index(
        op.f("ix_presentation_price_history_presentation_id"),
        table_name="presentation_price_history",
    )
    op.drop_index(
        op.f("ix_presentation_price_history_id"),
        table_name="presentation_price_history",
    )
    op.drop_table("presentation_price_history")

    op.drop_index(
        op.f("ix_order_details_presentation_id"), table_name="order_details"
    )
    op.drop_index(op.f("ix_order_details_order_id"), table_name="order_details")
    op.drop_index(op.f("ix_order_details_id"), table_name="order_details")
    op.drop_table("order_details")

    op.drop_index(
        op.f("ix_product_stock_movements_product_id"),
        table_name="product_stock_movements",
    )
    op.drop_index(
        op.f("ix_product_stock_movements_id"),
        table_name="product_stock_movements",
    )
    op.drop_table("product_stock_movements")

    op.drop_index(op.f("ix_presentations_product_id"), table_name="presentations")
    op.drop_index(op.f("ix_presentations_id"), table_name="presentations")
    op.drop_table("presentations")

    op.drop_index(op.f("ix_batch_costs_id"), table_name="batch_costs")
    op.drop_table("batch_costs")

    op.drop_index(op.f("ix_products_recipe_id"), table_name="products")
    op.drop_index(op.f("ix_products_id"), table_name="products")
    op.drop_table("products")

    op.drop_index(op.f("ix_orders_id"), table_name="orders")
    op.drop_index(op.f("ix_orders_customer_id"), table_name="orders")
    op.drop_table("orders")

    op.drop_index(
        op.f("ix_ingredient_stock_movements_ingredient_id"),
        table_name="ingredient_stock_movements",
    )
    op.drop_index(
        op.f("ix_ingredient_stock_movements_id"),
        table_name="ingredient_stock_movements",
    )
    op.drop_table("ingredient_stock_movements")

    op.drop_index(
        op.f("ix_ingredient_prices_ingredient_id"),
        table_name="ingredient_prices",
    )
    op.drop_index(op.f("ix_ingredient_prices_id"), table_name="ingredient_prices")
    op.drop_table("ingredient_prices")

    op.drop_index(op.f("ix_customers_id"), table_name="customers")
    op.drop_table("customers")