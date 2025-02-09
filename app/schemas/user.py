from pydantic import EmailStr, BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(min_length=5, max_length=30, description="Password (min 5, max 30)")
    city: str = Field(..., description="City name")
    info: str = Field(..., description="Info about user")
    photo: str | None = Field(None, description="Photo URL")


class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(min_length=5, max_length=30, description="Password (min 5, max 30)")


class UserResponse(BaseModel):
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email address")
    city: str = Field(..., description="City name")
    info: str = Field(..., description="Info about user")
    photo: str | None = Field(None, description="Photo URL")
