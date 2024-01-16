from sqlalchemy import Column, BigInteger, String, Integer, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False, nullable=False)
    username = Column(String(32), nullable=False)
    study_group = Column(String(32), nullable=False)
    language_code = Column(String(32), nullable=False)


class Class(Base):
    __tablename__ = "ClassSchedule"

    item_id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    study_group = Column(String(32), nullable=False)
    start_time = Column(DateTime, nullable=False)
    subject_name = Column(String(256), nullable=False)
    room = Column(String(32), nullable=True)
    teacher = Column(String(256), nullable=True)
    subgroup = Column(String(16), nullable=True)
