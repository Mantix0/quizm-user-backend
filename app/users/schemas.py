from datetime import datetime
from typing import TypeVar, Generic, List

from pydantic import BaseModel, EmailStr, Field

T = TypeVar("T", bound=BaseModel)


class UserRegistration(BaseModel):
    username: str = Field(
        ..., min_length=2, max_length=20, description="Имя пользователя"
    )
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )


class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(
        ..., min_length=5, max_length=50, description="Пароль, от 5 до 50 знаков"
    )


class RecordInput(BaseModel):
    quiz_id: int = Field(..., description="Id квиза")
    score: int = Field(..., description="Счёт в %")


class RecordReturn(BaseModel):
    id: int
    quiz_id: int = Field(..., description="Id квиза")
    score: int = Field(..., description="Счёт в %")
    created_at: datetime = Field(..., description="Дата создания")


class RecordReturnList:
    record = List[RecordReturn]


class UserReturn(BaseModel):
    username: str = Field(
        ..., min_length=2, max_length=20, description="Имя пользователя"
    )
    email: EmailStr = Field(..., description="Электронная почта")
    id: int


class AppResponse(BaseModel, Generic[T]):
    data: T


class AppResponseList(BaseModel, Generic[T]):
    data: List[T]
