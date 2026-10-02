from pydantic import BaseModel , EmailStr , Field

class UserCreation(BaseModel):

    username : str
    email : EmailStr
    password : str


class UserLogin(BaseModel):
    email : EmailStr = Field(description="holds user mail",strict=True)
    password :  str = Field(description="holds password")