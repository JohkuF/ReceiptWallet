from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    username: str
    email: str | None = None


class UserInDB(User):
    id: int
    hashed_password: str
    disabled: bool | None = False
