# Backend (SWAPI)

---
## Build & Run

### Containers

```
docker build . -t backend
docker run -d -p 3333:80 backend
```
### Local 

```
# create & use virtual environment
python -m venv venv
source venv/bin/activate

#install dependencies
pip install -r requirements.txt

# start app
uvicorn app.main:app --reload
```

