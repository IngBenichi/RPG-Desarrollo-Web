from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Personaje
from app.schemas import ApiResponse, PersonajeCreate, PersonajeOut, PersonajeUpdate

router = APIRouter(prefix="/personajes", tags=["Personajes"])


@router.post("", response_model=ApiResponse[PersonajeOut], status_code=201)
def crear_personaje(data: PersonajeCreate, db: Session = Depends(get_db)):
    personaje = Personaje(**data.model_dump())
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    return ApiResponse(
        success=True,
        message=f"Personaje '{personaje.nombre}' creado exitosamente con ID {personaje.id}.",
        data=PersonajeOut.model_validate(personaje),
    )


@router.get("", response_model=ApiResponse[list[PersonajeOut]])
def listar_personajes(db: Session = Depends(get_db)):
    personajes = db.query(Personaje).all()
    total = len(personajes)
    mensaje = f"Se encontraron {total} personaje(s) registrado(s)." if total else "No hay personajes registrados aún."
    return ApiResponse(
        success=True,
        message=mensaje,
        data=[PersonajeOut.model_validate(p) for p in personajes],
    )


@router.get("/{personaje_id}", response_model=ApiResponse[PersonajeOut])
def obtener_personaje(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.get(Personaje, personaje_id)
    if not personaje:
        raise HTTPException(
            status_code=404,
            detail=f"No existe ningún personaje con ID {personaje_id}.",
        )
    return ApiResponse(
        success=True,
        message=f"Personaje '{personaje.nombre}' encontrado.",
        data=PersonajeOut.model_validate(personaje),
    )


@router.put("/{personaje_id}", response_model=ApiResponse[PersonajeOut])
def actualizar_personaje(
    personaje_id: int, data: PersonajeUpdate, db: Session = Depends(get_db)
):
    personaje = db.get(Personaje, personaje_id)
    if not personaje:
        raise HTTPException(
            status_code=404,
            detail=f"No existe ningún personaje con ID {personaje_id}. No se pudo actualizar.",
        )
    campos_actualizados = list(data.model_dump(exclude_none=True).keys())
    for campo, valor in data.model_dump(exclude_none=True).items():
        setattr(personaje, campo, valor)
    db.commit()
    db.refresh(personaje)
    return ApiResponse(
        success=True,
        message=f"Personaje '{personaje.nombre}' actualizado correctamente. Campos modificados: {', '.join(campos_actualizados)}.",
        data=PersonajeOut.model_validate(personaje),
    )


@router.delete("/{personaje_id}", response_model=ApiResponse[None])
def eliminar_personaje(personaje_id: int, db: Session = Depends(get_db)):
    personaje = db.get(Personaje, personaje_id)
    if not personaje:
        raise HTTPException(
            status_code=404,
            detail=f"No existe ningún personaje con ID {personaje_id}. No se pudo eliminar.",
        )
    nombre = personaje.nombre
    db.delete(personaje)
    db.commit()
    return ApiResponse(
        success=True,
        message=f"El personaje '{nombre}' (ID {personaje_id}) fue eliminado permanentemente.",
    )
