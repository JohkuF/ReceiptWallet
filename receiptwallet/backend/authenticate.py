from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm.session import Session

from .constants import SECRET_KEY, ALGORITHM, PEPPER

from .db.get_db import get_db

from .schemas.user import UserInDB
from .db.base import User
from .schemas.token import TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password, "bcrypt")


def get_password_hash(password):
    return pwd_context.hash(password + PEPPER, "bcrypt")


def get_user(db: Session, username: str):
    user = db.query(User).filter_by(username=username).one_or_none()
    if user:
        return UserInDB(**user.__dict__)

    return None


def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False

    if not verify_password(password + PEPPER, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_schema), db: Session = Depends(get_db)
):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)

    except JWTError:
        raise credential_exception

    user = get_user(db, username=token_data.username)

    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return current_user
