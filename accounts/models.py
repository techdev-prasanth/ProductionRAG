from database.db_config import Base
from sqlalchemy import (
    String , Integer , DateTime , Boolean , func,
    ForeignKey,
    Text)

from sqlalchemy.orm import mapped_column , Mapped  ,relationship
from sqlalchemy.dialects.postgresql import UUID , JSONB
import uuid
from sqlalchemy import text

from datetime import datetime
from pydantic import EmailStr
from typing import Optional



class TimestampMixin(Base):
    __abstract__ = True

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),nullable=False)


    config = False

class User(TimestampMixin):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                        server_default=text("gen_random_uuid()")
                                           )

    username : Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    password : Mapped[str] = mapped_column(String(255),nullable=False)
    email : Mapped[str] = mapped_column(String(100),nullable=False,unique=True)
    last_login : Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True),default=None)
    is_active : Mapped[bool] = mapped_column(Boolean,default=True)
    profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    history : Mapped[dict] = mapped_column(JSONB,default=dict)



    def __str__(self) -> str:
        return f"{self.username} -{self.email}"



class UserProfile(TimestampMixin):

    __tablename__ = "user_profiles"
    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                        server_default=text("gen_random_uuid()")
                                           )

    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                           ForeignKey("users.id",ondelete="CASCADE"),
                                           nullable=False,
                                           unique=True
                                           )

    first_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="profile")




