from fastapi import Depends, status
from sqlalchemy import select, func
from sqlalchemy.orm.session import Session

from .base import Group, User, create_group_table
from .get_db import get_db


def new_group(db: Session, user_id: int, group_name: str) -> int:

    last_group_id_query = db.query(func.max(Group.group_id))
    last_group_id = db.execute(last_group_id_query).one()[0] or 0

    group = Group(
        user_id = user_id,
        group_id= last_group_id + 1,
        group_name=group_name
    )
    
    db.add(group)
    db.commit()
    
    return last_group_id + 1
    

def is_group(db: Session, user_id: int, group_name: str):
    """
    Check if user in group that has same name
    """
    
    query = select(Group.group_name).join(User).filter(User.id == user_id).filter(Group.group_name == group_name)
    result = db.execute(query).one_or_none()
    
    if result:
        return True
    return False
    