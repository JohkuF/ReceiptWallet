from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Table,
    MetaData,
    Float,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .get_db import engine

Base = declarative_base()
metadata = MetaData()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, index=True)
    disabled = Column(Boolean, default=False)


class Group(Base):
    __tablename__ = "groups"
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    group_id = Column(Integer,unique=True,index=True, primary_key=True)
    group_name = Column(String)


def create_group_table(group_id):
    class GroupTable(Base):
        __tablename__ = f"group_{group_id}"
        id = Column(Integer, primary_key=True)
        date = Column(String)
        product = Column(String)
        category = Column(String)
        price = Column(Float)
    
    GroupTable.metadata.create_all(bind=engine)
    

    return GroupTable