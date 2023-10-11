from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    MetaData,
    Float,
    ForeignKey,
)

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from .get_db import engine

Base = declarative_base()
metadata = MetaData()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String, index=True)
    disabled = Column(Boolean, default=False)

    # One-to-many relationship with Group
    groups = relationship("Group", back_populates="user")


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    group_id = Column(Integer, index=True)
    group_name = Column(String)

    # Many-to-one relationship with User
    user = relationship("User", back_populates="groups")

    # One-to-Many relationship with Product
    products = relationship("Product", back_populates="group")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey("groups.group_id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    date = Column(String)
    product = Column(String)
    category = Column(String)
    price = Column(Float)

    # Many-to-one relationship with Group
    group = relationship("Group", back_populates="products")
