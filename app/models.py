from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel


class FilmStarshipLink(SQLModel, table=True):
    film_episode_id: Optional[int] = Field(default=None, foreign_key="film.episode_id", primary_key=True)
    starship_id: Optional[int] = Field(default=None, foreign_key="starship.id", primary_key=True)


class Starship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cost_in_credits: int

    films: list["Film"] = Relationship(back_populates="starships", link_model=FilmStarshipLink)


class FilmBase(SQLModel):
    episode_id: int = Field(unique=True)
    title: str


class Film(FilmBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    starships: List["Starship"] = Relationship(back_populates="films", link_model=FilmStarshipLink)


class FilmPublic(FilmBase):
    starships: List[Starship]



