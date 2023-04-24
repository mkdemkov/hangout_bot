from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str
    budget: str