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

class Tenant(Base):
    __tablename__="tenants"