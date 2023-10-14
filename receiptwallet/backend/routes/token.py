from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm.session import Session

from ..db.get_db import get_db

from ..authenticate import authenticate_user, create_access_token
from ..constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ..schemas.token import Token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_accesss_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response.set_cookie(
        key="token",
        value=access_token,
    )
    return {"access_token": access_token, "token_type": "Bearer"}
