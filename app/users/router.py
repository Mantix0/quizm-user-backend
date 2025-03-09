from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi import Response

from .models import User, Record
from .schemas import (
    UserRegistration,
    UserAuth,
    AppResponse,
    UserReturn,
    RecordInput,
    RecordReturn,
    AppResponseList,
)
from .dao import UsersDAO, RecordsDAO
from .auth import get_password_hash, authenticate_user, create_access_token
from ..dependencies import get_active_user

router = APIRouter(prefix="/api/v1/users", tags=["Работа с пользователями"])


@router.get("/{user_id}/records", summary="Получить записи пользователя по user_id")
async def get_records_by_student_id(user_id: int) -> AppResponseList[RecordReturn]:
    records = await UsersDAO.get_user_records_by_id(user_id)
    return AppResponseList(
        data=[RecordReturn.model_validate(record.__dict__) for record in records]
    )


@router.post(":register/", summary="Зарегистрировать пользователя")
async def add_user(user_data: UserRegistration):
    user = await UsersDAO.get_user_by_email(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
        )
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {"message": "Вы успешно зарегистрированы!"}


@router.post(":login/", summary="Авторизовать пользователя")
async def auth_user(response: Response, user_data: UserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
        )
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "refresh_token": None}


@router.get(":current-user/", summary="Получить действующего пользователя")
async def get_current_user(
    user_data: User = Depends(get_active_user),
) -> AppResponse[UserReturn]:
    return AppResponse(data=UserReturn.model_validate(user_data.__dict__))


@router.post(
    ":current-user/records", summary="Добавить запись действующему пользователю"
)
async def get_records_by_student_id(
    record: RecordInput, user_data: User = Depends(get_active_user)
) -> AppResponse[RecordReturn]:
    new_record = await RecordsDAO.add(user_data, **record.model_dump())
    return AppResponse(data=RecordReturn.model_validate(new_record.__dict__))


@router.post(":logout/", summary="Деактивировать действующего пользователя")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "Пользователь успешно вышел из системы"}


router_records = APIRouter(prefix="/api/v1/records", tags=["Работа с записями"])


@router_records.get("/{item_id}", summary="Получить записи квиза по quiz_id")
async def get_records_by_quiz_id(item_id: int):
    return await UsersDAO.get_user_records_by_id(item_id)
