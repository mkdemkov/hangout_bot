import os
from database.entities.user import User
from sqlalchemy import create_engine, insert, update, select
from dotenv import load_dotenv


# Function to update state of user in database
def update_state(user_id, type=None, budget=None):
    load_dotenv()
    path = os.getenv('PATH_FOR_DB')
    engine = create_engine(path)
    if type is not None:
        statement = select(User).where(User.id == user_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchone()
        if result:
            statement = update(User).where(User.id == user_id).values(type=type)
        else:
            statement = insert(User).values(id=user_id, type=type)
        with engine.connect() as conn:
            conn.execute(statement)
    if budget is not None:
        statement = update(User).where(User.id == user_id).values(budget=budget)
        with engine.connect() as conn:
            conn.execute(statement)


# Function to get type of place and user's budget from database
def get_type_and_budget(user_id):
    load_dotenv()
    path = os.getenv('PATH_FOR_DB')
    engine = create_engine(path)
    statement = select(User.type).where(User.id == user_id)
    with engine.connect() as conn:
        type = conn.execute(statement).fetchone()
        statement = select(User.budget).where(User.id == user_id)
        budget = conn.execute(statement).fetchone()
        return type, budget
