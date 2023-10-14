from sqlalchemy import Table, text
from fastapi import HTTPException, status
from datetime import datetime

from fastapi import Depends, status
from sqlalchemy import select, func
from sqlalchemy.orm.session import Session

from .base import Group, User, Product

# from ..schemas.product import Product
from .get_db import get_db


async def new_group(db: Session, user_id: int, group_name: str) -> int:
    last_group_id_query = db.query(func.max(Group.group_id))
    last_group_id = db.execute(last_group_id_query).one()[0] or 0

    id_query = db.query(func.max(Group.id))
    last_id = db.execute(id_query).one()[0] or 0

    group = Group(
        id=last_id + 1,
        user_id=user_id,
        group_id=last_group_id + 1,
        group_name=group_name,
    )

    db.add(group)
    db.commit()

    return "Ok"


async def is_group(db: Session, user_id: int, group_name: str):
    """
    Check if user in group that has same name
    """

    query = (
        select(Group.group_name)
        .join(User)
        .filter(User.id == user_id)
        .filter(Group.group_name == group_name)
    )
    result = db.execute(query).one_or_none()

    if result:
        return True
    return False


async def add_product(db: Session, user_id: int, group_name: str, product):
    """
    To add product to db
    """
    try:
        # Get next product id
        id_query = db.query(func.max(Product.id))
        last_id = db.execute(id_query).one()[0] or 0

        # Get group_id by name
        id_query = (
            db.query(Group.group_id)
            .filter(Group.group_name == group_name)
            .filter(Group.user_id == user_id)
        )
        group_id = db.execute(id_query).one()[0]

        new_product = Product(
            id=last_id + 1,
            group_id=group_id,
            user_id=user_id,
            date=product.date,
            product=product.product,
            category=product.category,
            price=product.price,
        )

        db.add(new_product)
        db.commit()

        return "Ok"

    except Exception as e:
        print(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Something went wrong"
        )


async def add_user(db: Session, user_id, username, group_name):
    # Get user id
    query_id = db.query(User.id).filter(User.username == username)
    new_user_id = db.execute(query_id).one_or_none()

    # Get id
    id_query = db.query(func.max(Group.id))
    last_id = db.execute(id_query).one()[0]

    print(user_id, group_name)
    # get group id
    query_group_id = (
        db.query(Group.group_id)
        .filter(Group.user_id == user_id)
        .filter(Group.group_name == group_name)
    )
    group_id = db.execute(query_group_id).one()[0]

    if new_user_id:
        new_user = Group(
            id=last_id + 1,
            user_id=new_user_id[0],
            group_id=group_id,
            group_name=group_name,
        )

        db.add(new_user)
        db.commit()

        return "Ok"
