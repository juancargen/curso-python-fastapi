from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Aplicación con FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)


Base.metadata.create_all(bind=engine)


'''
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
'''

@app.get('/', tags=['home'], response_class=HTMLResponse)
def message():
    return """<h1>Hello World</h1>"""


