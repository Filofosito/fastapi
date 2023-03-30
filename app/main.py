from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import user, post, auth, vote

#va a tomar los modelos de la carpeta model y crear las tablas con sqlalchemy
#models.Base.metadata.create_all(bind=engine)
#si usamos alembic ya no es necesaria esta línea, sino esta otra:

app = FastAPI()

origins =["*"] #permite todos los orígenes para hacer pública la API y no tenga un CORS problem
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #permite todos los métodos
    allow_headers=["*"], #permite todas las cabeceras
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root(): #el nombre concreto no importa nada, procuremos que sea descriptivo
    return {"message": "Welcome to my api!!!"}


