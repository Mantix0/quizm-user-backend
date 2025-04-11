from datetime import datetime

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, " f"username={self.username!r},"
        )

    def __repr__(self):
        return str(self)


class Record(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship("User", backref="records")
    quiz_id: Mapped[int]
    quiz_name: Mapped[str] = mapped_column(nullable=True)
    score: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    def __str__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, "
            f"user_id={self.user_id!r},"
            f"quiz_id={self.quiz_id!r},"
            f"score={self.score!r}"
        )

    def __repr__(self):
        return str(self)
