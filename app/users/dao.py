from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy.future import select
from app.users.models import User
from .schemas import UserRegistration
from ..database import async_session


class UsersDAO:
    @classmethod
    async def add(cls, **values):
        async with async_session() as session:
            async with session.begin():
                new_instance = User(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def get_user_by_email(cls, email: str):
        async with async_session() as session:
            query = select(User).filter_by(email=email)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_user_by_id(cls, id: int):
        async with async_session() as session:
            query = select(User).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()


