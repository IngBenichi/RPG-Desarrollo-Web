from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None


class PersonajeBase(BaseModel):
    nombre: str = Field(..., examples=["Aragorn"])
    color_piel: str = Field(..., examples=["blanco"])
    raza: str = Field(..., examples=["Humano"])
    fuerza: float = Field(10.0, ge=0, le=100, examples=[85.0])
    agilidad: float = Field(10.0, ge=0, le=100, examples=[70.0])
    magia: float = Field(10.0, ge=0, le=100, examples=[20.0])
    conocimiento: float = Field(10.0, ge=0, le=100, examples=[75.0])


class PersonajeCreate(PersonajeBase):
    pass


class PersonajeUpdate(BaseModel):
    nombre: Optional[str] = None
    color_piel: Optional[str] = None
    raza: Optional[str] = None
    fuerza: Optional[float] = Field(None, ge=0, le=100)
    agilidad: Optional[float] = Field(None, ge=0, le=100)
    magia: Optional[float] = Field(None, ge=0, le=100)
    conocimiento: Optional[float] = Field(None, ge=0, le=100)


class PersonajeOut(PersonajeBase):
    id: int

    model_config = {"from_attributes": True}


class BatallaRequest(BaseModel):
    id_personaje_1: int
    id_personaje_2: int


class ResultadoBatalla(BaseModel):
    ganador: PersonajeOut
    perdedor: PersonajeOut
    puntaje_ganador: float
    puntaje_perdedor: float
    diferencia: float
    resumen: str
    resumen: str
