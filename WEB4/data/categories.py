import sqlalchemy as sa
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase):
    __tablename__ = 'categories'
    __table_args__ = {'extend_existing': True}
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    jobs = orm.relationship("Jobs", secondary="association", back_populates="categories")