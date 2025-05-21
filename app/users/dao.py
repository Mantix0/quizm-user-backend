from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from app.users.models import User, Record
from ..database import async_session


class UsersDAO:
    @classmethod
    async def add(cls, user_dict, session: AsyncSession):
        new_instance = User(**user_dict)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def get_user_by_email(cls, email: str, session: AsyncSession):
        query = select(User).filter_by(email=email)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_user_by_id(cls, id: int, session: AsyncSession):
        query = select(User).filter_by(id=id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_user_records_by_id(cls, id: int, session: AsyncSession):
        query = select(Record).filter_by(user_id=id).order_by(Record.created_at.desc())
        result = await session.execute(query)
        return result.scalars().all()


class RecordsDAO:
    @classmethod
    async def get_records_by_id(cls, quiz_id: int, session: AsyncSession):
        query = select(Record).filter_by(quiz_id=quiz_id).order_by(Record.score.desc())
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, user: User, record_dict, session: AsyncSession):
        new_instance = Record(user_id=user.__dict__["id"], **record_dict)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance
