from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.schemas import UserResponse, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user_services import get_current_user
from app.core.database import get_db
from app.models.models import User
from app.services.user_services import create_normal_user

router = APIRouter(
    prefix= "/users",
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def add_a_team_member(
    data_model:UserCreate, 
    current_user:User = Depends(get_current_user),
    db:AsyncSession=Depends(get_db)):


    if current_user.role not in ["OWNER", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail= "Only workspace Owners or admins can add team members"
        )


    new_member = await create_normal_user(

        data_model = data_model,
        tenant_id =current_user.tenant_id,
        db=db


    )

    return new_member
