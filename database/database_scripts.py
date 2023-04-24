import os
from database.entities.user import User
from sqlalchemy import create_engine, insert, update, select
from dotenv import load_dotenv


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
    # statement = update(User).where(User.id == 5).values(state='new_state')
    # statement = insert(User).values(id=5, state='not active')


if __name__ == '__main__':
    update_state(0, 2)
