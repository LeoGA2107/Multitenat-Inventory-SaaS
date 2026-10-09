from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional

# User schemas

class TenantUserCreate(BaseModel):
    company_name:str
    slug:str
    name:str
    email:EmailStr
    phone_number:Optional[str]=None
    role:str
    password:str

class UserCreate(BaseModel):
    name:str
    email:EmailStr
    tenant_id:int
    phone_number:Optional[str]=None
    password:str

class UserResponse(BaseModel):
    name:str
    user_id:int
    email:EmailStr
    tenant_id:int
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes = True)


# Tenant schemas

class TenantCreate(BaseModel):
    name:str
    slug:str

class TenantResponse(BaseModel):
    tenant_id:int
    name:str
    slug:str
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)


class GetUser(BaseModel):
    user:str

