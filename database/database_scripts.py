import os
from database.entities.user import User
from sqlalchemy import create_engine, insert, update, select
from dotenv import load_dotenv
from location.location_parser import get_distance_in_metres


# Function to update state of user in database
def update_state(user_id, type=None, distance=None):
    load_dotenv()
    path = os.getenv('PATH_FOR_DB')
    engine = create_engine(path)
    distance = get_distance_in_metres(distance)
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
    if distance is not None:
        statement = update(User).where(User.id == user_id).values(distance=distance)
        with engine.connect() as conn:
            conn.execute(statement)


# Function to get type of place and user's budget from database
def get_type_and_distance(user_id):
    load_dotenv()
    path = os.getenv('PATH_FOR_DB')
    engine = create_engine(path)
    statement = select(User.type).where(User.id == user_id)
    with engine.connect() as conn:
        type = conn.execute(statement).fetchone()
        statement = select(User.distance).where(User.id == user_id)
        distance = conn.execute(statement).fetchone()
        return type, distance
