from fastapi import APIRouter, Depends
from pydantic import SecretStr
from sqlalchemy.orm.session import Session


from ..db.get_db import get_db
from ..schemas.user import User, UserInDB
from ..authenticate import get_current_active_user
from ..authenticate import get_password_hash
from ..db.user import add_user

router = APIRouter()


@router.get("/profile", response_model=User)
async def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/signup")
async def signup_user(
    username: str, email: str, password: SecretStr, db: Session = Depends(get_db)
):
    hashed_password = get_password_hash(password.get_secret_value())
    return add_user(db, username, email, hashed_password)
