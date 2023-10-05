from fastapi import APIRouter, Depends, status, BackgroundTasks

from fastapi.exceptions import HTTPException
from pydantic import SecretStr
from sqlalchemy.orm.session import Session


from ..db.get_db import get_db
from ..db.base import create_group_table
from ..schemas.user import User, UserInDB
from ..authenticate import get_current_active_user
from ..authenticate import get_password_hash
from ..db.groups import new_group, is_group

router = APIRouter()


@router.post("/group/new", status_code=status.HTTP_201_CREATED)
def make_new_group(
    group_name: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Check if group already exists
    if is_group(db, current_user.id, group_name):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Group already exists")
    
    group_id = new_group(db, current_user.id, group_name)
    
    
    background_tasks.add_task(create_group_table, group_id)
    
    return 'Ok'

#@router.post("/group/{group_name}/add")
#def add_item(group_name: str, )
