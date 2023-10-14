from fastapi import APIRouter, Depends, status, BackgroundTasks, Request
from fastapi.exceptions import HTTPException


from pydantic import SecretStr
from sqlalchemy.orm.session import Session

from ..schemas.product import Product
from ..db.get_db import get_db
from ..db.groups import add_product
from ..db.user import get_user_groups
from ..schemas.user import UserInDB, UserInDB
from ..authenticate import get_current_active_user
from ..authenticate import get_password_hash
from ..db.groups import new_group, is_group, add_user, get_products

router = APIRouter()


@router.get("/groups/")
async def get_groups(
    request: Request,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return await get_user_groups(db, current_user.id)


# @router.get('/group/{group_name}/receipts')
# @router.get('/group/{group_name}/bills')
# @router.get('/group/{group_name}/info')


@router.get("/group/{group_name}/products")
async def get_group_products(
    group_name,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    return await get_products(group_name, current_user.id, db)


@router.post("/group/new", status_code=status.HTTP_201_CREATED)
async def make_new_group(
    group_name: str,
    # background_tasks: BackgroundTasks,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Check if group already exists
    if await is_group(db, current_user.id, group_name):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Group already exists")

    return await new_group(db, current_user.id, group_name)


@router.get("/group/{group_name}/add/user")
async def app_user(
    group_name: str,
    username: str,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Check if group exists
    if not await is_group(db, current_user.id, group_name):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Group does not exist")

    return await add_user(db, current_user.id, username, group_name)


@router.post("/group/{group_name}/add/product")
async def add_item(
    group_name: str,
    product: Product,
    current_user: UserInDB = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Check if group exists
    if not await is_group(db, current_user.id, group_name):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Group does not exist")

    return await add_product(db, current_user.id, group_name, product)
