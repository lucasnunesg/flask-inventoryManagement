"""added `amount_in_stock` column to products table

Revision ID: c5ed98a8f947
Revises: f1ec23dce0a6
Create Date: 2023-12-16 11:40:29.428151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c5ed98a8f947'
down_revision = 'f1ec23dce0a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_product')
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount_in_stock', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.drop_column('amount_in_stock')

    op.create_table('order_product',
    sa.Column('order_id', sa.INTEGER(), nullable=False),
    sa.Column('product_id', sa.INTEGER(), nullable=False),
    sa.Column('product_amount', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
    sa.PrimaryKeyConstraint('order_id', 'product_id')
    )
    # ### end Alembic commands ###