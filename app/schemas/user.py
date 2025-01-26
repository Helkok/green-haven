from pydantic import EmailStr, BaseModel


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    city: str
    info: str
    photo: str | None


class LoginRequest(BaseModel):
    email: str
    password: str
