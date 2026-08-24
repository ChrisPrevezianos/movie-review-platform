import uuid
from sqlmodel import Field, SQLModel


class Genre(SQLModel, table=True):
    __tablename__ = "genres"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=100)