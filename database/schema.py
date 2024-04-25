import uuid
from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'taxbot_users'

    id: Mapped[str] = mapped_column('id', String(36), insert_default=str(uuid.uuid4()), primary_key=True)
    chat_id: Mapped[int] = mapped_column('chat_id', Integer())
    username: Mapped[str] = mapped_column('username', String())
    firstname: Mapped[str] = mapped_column('firstname', String())
    created_at: Mapped[datetime] = mapped_column('created_at', DateTime(timezone=True), insert_default=datetime.now())

    def __repr__(self) -> str:
        return f"User(uuid={self.id!r}, chat_id={self.chat_id!r}, username={self.username!r}), firstname={self.firstname!r}, created_at={self.created_at!r}"
