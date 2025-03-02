from fastapi import APIRouter, HTTPException, status, Depends
from fastapi import Response

from .models import User
from .schemas import UserRegistration, UserAuth
from .dao import UsersDAO
from .auth import get_password_hash, authenticate_user, create_access_token
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/v1/users", tags=["Работа с пользователями"])


@router.get(f"/{id}", summary="Получить пользователя по email")
async def get_student_by_id(email: str):
    return await UsersDAO.get_student_by_email(email)


@router.post("/register/", summary="Зарегистрировать пользователя")
async def add_user(user_data: UserRegistration):
    user = await UsersDAO.get_user_by_email(email=user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Пользователь уже существует'
        )
    user_dict = user_data.model_dump()
    user_dict['password'] = get_password_hash(user_data.password)
    await UsersDAO.add(**user_dict)
    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login/")
async def auth_user(response: Response, user_data: UserAuth):
    check = await authenticate_user(email=user_data.email, password=user_data.password)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Неверная почта или пароль')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'access_token': access_token, 'refresh_token': None}


@router.get("/current-user/")
async def get_current_user(user_data: User = Depends(get_current_user)):
    return user_data


@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Пользователь успешно вышел из системы'}
