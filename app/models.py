from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Personaje(Base):
    __tablename__ = "personajes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    color_piel = Column(String, nullable=False)
    raza = Column(String, nullable=False)
    fuerza = Column(Float, nullable=False, default=10.0)
    agilidad = Column(Float, nullable=False, default=10.0)
    magia = Column(Float, nullable=False, default=10.0)
    conocimiento = Column(Float, nullable=False, default=10.0)
