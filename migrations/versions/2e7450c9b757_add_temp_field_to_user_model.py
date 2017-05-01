"""Add temp field to User model

Revision ID: 2e7450c9b757
Revises: 
Create Date: 2017-05-01 20:38:35.195208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e7450c9b757'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('temp_field', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'temp_field')
    # ### end Alembic commands ###
