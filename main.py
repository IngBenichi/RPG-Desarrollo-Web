from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, SessionLocal, engine, seed_db
from app.routers import batallas, personajes


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_db(db)
    yield


app = FastAPI(
    title="RPG Character API",
    description="Gestión de personajes y sistema de batallas para un juego de rol",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(personajes.router)
app.include_router(batallas.router)
