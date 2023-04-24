from sqlmodel import SQLModel, Field


# Class that represent table in database
class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    type: str  # type of establishment
    budget: str
