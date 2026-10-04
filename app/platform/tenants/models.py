from typing import List, Optional
from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.core.database import Base
from datetime import datetime

class TimestampMixin:
    created_at:Mapped[datetime] = mapped_column(server_default = func.now())
    updated_at:Mapped[datetime] = mapped_column(
        server_default = func.now(),
        onupdate=func.now())

class Tenant(Base, TimestampMixin):
    __tablename__="tenants"
    tenant_id : Mapped[int] = mapped_column(index=True, primary_key=True)
    name : Mapped[str] = mapped_column()
    slug: Mapped[str]= mapped_column(unique=True, index=True)
    users: Mapped[List["User"]]=relationship(back_populates="tenant")


class User(Base, TimestampMixin):
    __tablename__="users"
    user_id : Mapped[int]=mapped_column(index=True, primary_key=True)
    name : Mapped[str]=mapped_column()
    email : Mapped[str] = mapped_column(unique = True, index=True)
    password : Mapped [str]=mapped_column()

    tenant: Mapped["Tenant"]=relationship(back_populates="users")
    tenant_id: Mapped[int]=mapped_column(ForeignKey("tenants.tenant_id"), index = True)