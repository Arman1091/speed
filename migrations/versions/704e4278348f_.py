"""empty message

Revision ID: 704e4278348f
Revises: 
Create Date: 2024-06-09 20:08:31.740195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '704e4278348f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commande', schema=None) as batch_op:
        batch_op.add_column(sa.Column('prix_livr_ht', sa.Float(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commande', schema=None) as batch_op:
        batch_op.drop_column('prix_livr_ht')

    # ### end Alembic commands ###
