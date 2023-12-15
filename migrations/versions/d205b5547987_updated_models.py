"""updated models

Revision ID: d205b5547987
Revises: 5e755d21e1bf
Create Date: 2023-12-14 22:27:36.966155

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd205b5547987'
down_revision = '5e755d21e1bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=500), nullable=False),
    sa.Column('postcode', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('shipped_date', sa.DateTime(), nullable=True),
    sa.Column('delivered_date', sa.DateTime(), nullable=True),
    sa.Column('coupon_code', sa.String(length=50), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_product',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('order_id', 'product_id')
    )
    op.drop_table('inventory_item')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory_item',
    sa.Column('sku', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(), nullable=False),
    sa.Column('unit_cost', sa.FLOAT(), nullable=False),
    sa.Column('amount_in_stock', sa.INTEGER(), nullable=False),
    sa.Column('amount_sold', sa.INTEGER(), nullable=False),
    sa.Column('revenue', sa.FLOAT(), nullable=False),
    sa.Column('latest_sale', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('sku'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('order_product')
    op.drop_table('order')
    op.drop_table('product')
    op.drop_table('customer')
    # ### end Alembic commands ###