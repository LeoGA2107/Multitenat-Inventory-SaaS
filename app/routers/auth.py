from fastapi import APIRouter, status, HTTPException, Depends
from app.schemas.schemas import TenantResponse, TenantUserCreate, TenantAndOwner
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.authentication.create_and_login import create_owner_and_tenant


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TenantAndOwner)

async def register_tenant_and_owner(data_model:TenantUserCreate, db:AsyncSession=Depends(get_db)):

    result = await create_owner_and_tenant(data_model=data_model, db=db)
    return result
