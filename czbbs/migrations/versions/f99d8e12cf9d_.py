"""empty message

Revision ID: f99d8e12cf9d
Revises: 
Create Date: 2018-06-21 12:23:45.989120

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f99d8e12cf9d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userprofile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('realname', sa.String(length=50), nullable=True),
    sa.Column('qq', sa.String(length=20), nullable=True),
    sa.Column('singature', sa.String(length=100), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('user_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['front_user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userprofile')
    # ### end Alembic commands ###