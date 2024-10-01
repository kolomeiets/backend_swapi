from sqlmodel import Session
from .database import engine

# Returns DB session
def get_session():
    with Session(engine) as session:
        yield session


