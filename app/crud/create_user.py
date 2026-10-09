from sqlalchemy.ext.asyncio import AsyncSession
from app.platform.tenants.models import User
from app.platform.tenants.schemas import UserCreate
from app.modules.auth.security import hash_password
from app.core.database import get_db
from fastapi import Depends
from sqlalchemy import select



async def create_user(data_model: UserCreate, db:AsyncSession=Depends(get_db)):

    check_if_user_exist = select(User).where(User.username == data_model.name)
    results = await db.scalars(check_if_user_exist)
    fetch_user = results.first()


    if fetch_user:
        return "User already exist"


    password = hash_password(data_model.password)

    new_user = User(
        user = data_model.user,
        email = data_model.email,
        phone_number = data_model.phone_number,
        password = password.decode('utf-8')
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

    