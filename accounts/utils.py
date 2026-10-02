from datetime import datetime , timedelta , timezone
from typing import Annotated
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError , jwt
from config.settings import settings
from database.db_config import get_session
from sqlalchemy import select
from accounts.models import User
from fastapi import Depends , HTTPException 
from sqlalchemy.orm import Session
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS=settings.REFRESH_TOKEN_EXPIRE_DAYS


password_hash = PasswordHash.recommended()
def hash_password(password : str):
    return password_hash.hash(password=password)


def verify_password(plain_password,hased_password):
    return password_hash.verify(plain_password,hased_password)


def gen_access_token(data : dict):
    payload = data

    payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)


def gen_refresh_token(data: dict):
    payload = data.dict()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    payload["type"] = "refresh"

    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)



oauth2scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(
    token: str = Depends(oauth2scheme),
    db: Session = Depends(get_session),
):

    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.scalar(select(User).where(User.email == email))

    if user is None:
        raise credentials_exception

    return user