from sqlmodel import select
import requests
from .models import Starship, Film
from .dependencies import get_session


# Parser for SWAPI (https://swapi.info/)
async def parse_swapi():
    session = next(get_session())

    # read starships
    response = requests.get("https://swapi.info/api/starships/all.json")
    for starship in response.json():
        starship['id'] = starship['url'].replace("https://swapi.info/api/starships/", "")
        if not starship['cost_in_credits'].isdigit():
            starship['cost_in_credits'] = 0

        try:
            starship_db = Starship.model_validate(starship)
            session.add(starship_db)
        except Exception as e:
            print(e)

    try:
        session.commit()
    except Exception as error:
        # SWAPI Starships DB already in place
        return {"error": "SWAPI Starships DB already in place"}

    # read films
    response = requests.get("https://swapi.info/api/films/all.json")
    for film in response.json():
        try:
            film_db = Film.model_validate(film)

            starship_ids = []
            for s in film['starships']:
                starship_ids.append(s.replace("https://swapi.info/api/starships/", ""))

            starships = session.exec(select(Starship).where(Starship.id.in_(starship_ids))).all()
            for starship in starships:
                film_db.starships.append(starship)
            session.add(film_db)
            session.commit()

        except Exception as e:
            return {"error": "SWAPI Films DB already in place"}

    return {"success": "SWAPI has been parsed successfully"}
