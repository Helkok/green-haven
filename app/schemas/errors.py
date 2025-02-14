from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    errors: str = Field(..., description="Сообщение об ошибке, описывающее проблему.")
