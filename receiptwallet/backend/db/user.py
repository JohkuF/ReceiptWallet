from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError

from .base import User
from .get_db import get_db


def add_user(db: Session, username, email, hashed_password, disabled=False):
    # TODO Improve Error handling
    try:
        last_id_query = db.query(func.max(User.id))
        last_id = db.execute(last_id_query).one()[0] or 0

        new_user = User(
            id=last_id + 1,
            username=username,
            email=email,
            hashed_password=hashed_password,
            disabled=disabled,
        )

        db.add(new_user)
        db.commit()
    except IntegrityError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Username has already been taken"
        )

    return True
