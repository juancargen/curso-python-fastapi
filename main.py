from fastapi import FastAPI, Body, Path, Query, HTTPException, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Coroutine, Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer

app = FastAPI()
app.title = "Aplicación con FastAPI"
app.version = "0.0.1"

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail="Credenciales no válidas")

class User(BaseModel):
    email: str
    password: str

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(le=10, ge=0)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Mi película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 6.8,
                "category": "Acción"
            }
        }

movies = [
    {
        'id': 1,
        'title': 'Avatar1',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar2',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    }
]

@app.get('/', tags=['home'], response_class=HTMLResponse)
def message():
    return """<h1>Hello World</h1>"""

@app.post('/login', tags=['auth'])
def login(user: User):
    if (user.email == 'admin@gmail.com' and user.password == 'admin'):
        token = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)

@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    #return movies
    return JSONResponse(status_code=200, content=movies)

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id:int = Path(ge=1, le=2000)) -> Movie:
    for movie in movies:
        if movie['id'] == id:
            #return movie
            return JSONResponse(content=movie)
    #return []
    return JSONResponse(status_code=404, content=[])

@app.get('/movies/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    #return [movie for movie in movies if movie['category'] == category]
    data = [movie for movie in movies if movie['category'] == category]
    return JSONResponse(content=data)

@app.post('/movies', tags=['movies'], response_model=dict, status_code=201)
#def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
#
#    movies.append({
#        "id": id,
#        "title": title,
#        "overview": overview,
#        "year": year,
#        "rating": rating,
#        "category": category
#    })
#   return movies
def create_movie(movie: Movie) -> dict:
    movies.append(movie.model_dump())
    #return movies
    return JSONResponse(status_code=201, content={"message": "Se ha creado la película"})

@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
#def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
#    for movie in movies:
#        if movie['id'] == id:
#            movie['title'] = title
#            movie['overview'] = overview
#            movie['year'] = year
#            movie['rating'] = rating
#            movie['category'] = category
#            return movies
def update_movie(id: int, movie: Movie) -> dict:
    
    for item in movies:
        if item['id'] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            #return movies
            return JSONResponse(status_code=200, content={"message": "Se ha actualizado la película"})
    raise HTTPException(status_code=404, detail="Película no encontrada")

@app.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            #return movies
            return JSONResponse(status_code=200, content={"message": "Se ha eliminado la película"})
    raise HTTPException(status_code=404, detail="Película no encontrada")