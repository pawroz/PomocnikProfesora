"""empty message

Revision ID: 0d8260220c40
Revises: 
Create Date: 2020-10-29 15:11:56.193910

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d8260220c40'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_email', sa.String(length=64), nullable=True),
    sa.Column('teacher_email', sa.String(length=64), nullable=True),
    sa.Column('student_name', sa.String(length=64), nullable=True),
    sa.Column('student_surname', sa.String(length=64), nullable=True),
    sa.Column('teacher_name', sa.String(length=64), nullable=True),
    sa.Column('teacher_surname', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('time', sa.String(length=64), nullable=True),
    sa.Column('end_time', sa.String(length=64), nullable=True),
    sa.Column('reason', sa.String(length=64), nullable=True),
    sa.Column('decision', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_entries_date'), 'entries', ['date'], unique=False)
    op.create_index(op.f('ix_entries_decision'), 'entries', ['decision'], unique=False)
    op.create_index(op.f('ix_entries_end_time'), 'entries', ['end_time'], unique=False)
    op.create_index(op.f('ix_entries_reason'), 'entries', ['reason'], unique=False)
    op.create_index(op.f('ix_entries_student_email'), 'entries', ['student_email'], unique=False)
    op.create_index(op.f('ix_entries_student_name'), 'entries', ['student_name'], unique=False)
    op.create_index(op.f('ix_entries_student_surname'), 'entries', ['student_surname'], unique=False)
    op.create_index(op.f('ix_entries_teacher_email'), 'entries', ['teacher_email'], unique=False)
    op.create_index(op.f('ix_entries_teacher_name'), 'entries', ['teacher_name'], unique=False)
    op.create_index(op.f('ix_entries_teacher_surname'), 'entries', ['teacher_surname'], unique=False)
    op.create_index(op.f('ix_entries_time'), 'entries', ['time'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('surname', sa.String(length=64), nullable=True),
    sa.Column('date', sa.String(length=64), nullable=True),
    sa.Column('time', sa.String(length=64), nullable=True),
    sa.Column('end_time', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('permission', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_date'), 'users', ['date'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_end_time'), 'users', ['end_time'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_index(op.f('ix_users_permission'), 'users', ['permission'], unique=False)
    op.create_index(op.f('ix_users_surname'), 'users', ['surname'], unique=False)
    op.create_index(op.f('ix_users_time'), 'users', ['time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_time'), table_name='users')
    op.drop_index(op.f('ix_users_surname'), table_name='users')
    op.drop_index(op.f('ix_users_permission'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_end_time'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_date'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_entries_time'), table_name='entries')
    op.drop_index(op.f('ix_entries_teacher_surname'), table_name='entries')
    op.drop_index(op.f('ix_entries_teacher_name'), table_name='entries')
    op.drop_index(op.f('ix_entries_teacher_email'), table_name='entries')
    op.drop_index(op.f('ix_entries_student_surname'), table_name='entries')
    op.drop_index(op.f('ix_entries_student_name'), table_name='entries')
    op.drop_index(op.f('ix_entries_student_email'), table_name='entries')
    op.drop_index(op.f('ix_entries_reason'), table_name='entries')
    op.drop_index(op.f('ix_entries_end_time'), table_name='entries')
    op.drop_index(op.f('ix_entries_decision'), table_name='entries')
    op.drop_index(op.f('ix_entries_date'), table_name='entries')
    op.drop_table('entries')
    # ### end Alembic commands ###