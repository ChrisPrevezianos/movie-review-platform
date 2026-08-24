import datetime
import uuid
from sqlmodel import Field, SQLModel

class Director(SQLModel, table=True):
    __tablename__ = "directors"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    last_name: str = Field(index=True, max_length=50)
    first_name: str = Field(index=True, max_length=50)
    birth_date: datetime.date | None = Field(default=None)