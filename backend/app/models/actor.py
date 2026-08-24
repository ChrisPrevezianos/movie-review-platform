import datetime
import uuid
from sqlmodel import Field, SQLModel

class Actor(SQLModel, table=True):
    __tablename__ = "actors"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str = Field(index=True, max_length=50)
    last_name: str = Field(index=True, max_length=50)
    birth_date: datetime.date | None = Field(default=None, index=True) 