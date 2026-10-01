from database.db_config import Base
from sqlalchemy import String , Integer
from sqlalchemy.orm import mapped_column , Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import text

from datetime import datetime
from pydantic import EmailStr

class User(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                           primary_key=True,
                                        server_default=text("get_random_uuid()")
                                           )

    username : Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    email : Mapped[EmailStr] = mapped_column(String(100),nullable=False,unique=True)
    last_login : Mapped[datetime.datetime]