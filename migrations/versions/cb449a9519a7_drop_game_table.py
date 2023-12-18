"""Drop Game table

Revision ID: cb449a9519a7
Revises: 9660bbd16fb4
Create Date: 2023-12-13 13:14:32.414930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb449a9519a7'
down_revision = '9660bbd16fb4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('week', sa.INTEGER(), nullable=True),
    sa.Column('round', sa.INTEGER(), nullable=True),
    sa.Column('team1_id', sa.INTEGER(), nullable=True),
    sa.Column('team1_seed', sa.INTEGER(), nullable=True),
    sa.Column('team2_seed', sa.INTEGER(), nullable=True),
    sa.Column('team2_id', sa.INTEGER(), nullable=True),
    sa.Column('team1_score', sa.INTEGER(), nullable=True),
    sa.Column('team2_score', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.VARCHAR(length=50), nullable=True),
    sa.Column('winner_team_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['team1_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['team2_id'], ['team.id'], ),
    sa.ForeignKeyConstraint(['winner_team_id'], ['team.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###