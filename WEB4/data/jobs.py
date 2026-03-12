import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from . import association


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'
    __table_args__ = {'extend_existing': True}
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    team_leader = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    job = sa.Column(sa.String, nullable=True)
    work_size = sa.Column(sa.Integer, nullable=True)
    collaborators = sa.Column(sa.String, nullable=True)
    start_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    end_date = sa.Column(sa.DateTime, nullable=True)
    is_finished = sa.Column(sa.Boolean, default=False)
    user = orm.relationship("User", back_populates="jobs")
    categories = orm.relationship("Category", secondary="association", back_populates="jobs")