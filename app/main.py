from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session, select
from .database import engine
from .dependencies import get_session
from typing import List
from .models import Film, FilmPublic, Starship
from .parser import parse_swapi
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # create_db_and_tables()
    SQLModel.metadata.create_all(engine)
    await parse_swapi()


@app.get("/")
async def root():
    return {"index": "Hello"}


@app.get("/galactic-spending", response_model=List[FilmPublic])
async def galactic_spending(*, session: Session = Depends(get_session)):

    films = session.exec(select(Film).order_by(Film.episode_id)).all()


    return films
