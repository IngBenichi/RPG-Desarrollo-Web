from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Datos iniciales
# ---------------------------------------------------------------------------

PERSONAJES_INICIALES = [
    {"nombre": "Aragorn",  "color_piel": "blanco", "raza": "Humano", "fuerza": 85.0, "agilidad": 70.0, "magia": 20.0, "conocimiento": 75.0},
    {"nombre": "Legolas",  "color_piel": "blanco", "raza": "Elfo",   "fuerza": 60.0, "agilidad": 95.0, "magia": 40.0, "conocimiento": 80.0},
    {"nombre": "Gimli",    "color_piel": "blanco", "raza": "Enano",  "fuerza": 90.0, "agilidad": 45.0, "magia": 10.0, "conocimiento": 60.0},
    {"nombre": "Gandalf",  "color_piel": "blanco", "raza": "Mago",   "fuerza": 50.0, "agilidad": 55.0, "magia": 98.0, "conocimiento": 99.0},
    {"nombre": "Sauron",   "color_piel": "negro",  "raza": "Ainur",  "fuerza": 95.0, "agilidad": 65.0, "magia": 95.0, "conocimiento": 90.0},
]


def seed_db(db: Session) -> None:
    """Inserta los personajes iniciales solo si la tabla está vacía."""
    from app.models import Personaje  # import local para evitar ciclos

    if db.query(Personaje).count() == 0:
        for data in PERSONAJES_INICIALES:
            db.add(Personaje(**data))
        db.commit()


# ---------------------------------------------------------------------------
# Dependencia de sesión para FastAPI
# ---------------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
