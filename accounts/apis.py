from fastapi import APIRouter , Depends 
from fastapi.responses import JSONResponse
from accounts.models import User,UserProfile 
from accounts.schema import UserCreation , UserLogin
from database.db_config import get_session , get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from accounts.utils import hash_password , gen_access_token , gen_refresh_token, get_current_user
from fastapi import status
from sqlalchemy.exc import IntegrityError
from accounts.utils import verify_password
from sqlalchemy import select
import json
router = APIRouter(prefix="/api/v1/auth",tags=["auth"])


@router.post("/signup")
async def create_account(request: UserCreation,
                        session: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(request.password)
    user = User(username=request.username,
                        password=hashed_password,
                        email=str(request.email))
    try:
       

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return {
            "message":"account has been created",
            "status":status.HTTP_201_CREATED
        }
    except IntegrityError as e:
        await session.rollback()
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": f"Username or email already exists.{e}"}
        )
    except Exception as e:
        await session.rollback()
        print("errro",e)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"An internal error occurred during registration. {e}"}
        )


@router.post("/login")
async def login(request: UserLogin ,
           session : AsyncSession = Depends(get_db)):

    
    email = request.email
    password = request.password

    result = await session.execute(select(User).where(User.email == email))

    get_user = result.scalar_one_or_none()

    if not get_user:
        return JSONResponse(content="Account doesn't exist.",status_code=status.HTTP_400_BAD_REQUEST)
    
    if not verify_password(plain_password=password,
                           hased_password=get_user.password):
        return JSONResponse(content="Invalid Credentials",status_code=status.HTTP_401_UNAUTHORIZED)


    

    data = {
        "id":str(get_user.id),
        "email":get_user.email,
        "username":get_user.username
    }

    print("data",type(data))

    access_token = gen_access_token(data)

    return {
        "message":"login successfull.",
        "access_token":access_token
    }



@router.get("/profiles")
def get_profile(session : Session = Depends(get_session)):
    result = session.execute(select(UserProfile))
    profiles = result.scalars().all()

    return {
        "message":"user profile are fetched.",
        "status_code":status.HTTP_200_OK,
        "data":profiles
    }