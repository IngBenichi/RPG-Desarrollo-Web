from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Personaje
from app.schemas import ApiResponse, BatallaRequest, PersonajeOut, ResultadoBatalla

router = APIRouter(prefix="/batallas", tags=["Batallas"])


def calcular_puntaje(p: Personaje) -> float:
    """
    Fórmula de combate:
      - Fuerza      (35 %): daño físico directo
      - Agilidad    (25 %): probabilidad de evadir ataques
      - Magia       (25 %): ataques especiales / daño elemental
      - Conocimiento(15 %): bonus estratégico como multiplicador (+20 % máx.)
    """
    bonus = 1 + (p.conocimiento / 100) * 0.20
    puntaje = (p.fuerza * 0.35 + p.agilidad * 0.25 + p.magia * 0.25) * bonus
    return round(puntaje, 2)


@router.post("", response_model=ApiResponse[ResultadoBatalla])
def simular_batalla(data: BatallaRequest, db: Session = Depends(get_db)):
    p1 = db.get(Personaje, data.id_personaje_1)
    p2 = db.get(Personaje, data.id_personaje_2)

    if not p1:
        raise HTTPException(
            status_code=404,
            detail=f"No existe ningún personaje con ID {data.id_personaje_1}. Verifica el ID e intenta de nuevo.",
        )
    if not p2:
        raise HTTPException(
            status_code=404,
            detail=f"No existe ningún personaje con ID {data.id_personaje_2}. Verifica el ID e intenta de nuevo.",
        )
    if p1.id == p2.id:
        raise HTTPException(
            status_code=400,
            detail=f"El personaje '{p1.nombre}' no puede enfrentarse a sí mismo. Elige dos personajes distintos.",
        )

    puntaje1 = calcular_puntaje(p1)
    puntaje2 = calcular_puntaje(p2)

    if puntaje1 == puntaje2:
        raise HTTPException(
            status_code=400,
            detail=f"'{p1.nombre}' y '{p2.nombre}' tienen el mismo puntaje de combate ({puntaje1}). La batalla terminó en empate.",
        )

    ganador, perdedor = (p1, p2) if puntaje1 > puntaje2 else (p2, p1)
    pg = max(puntaje1, puntaje2)
    pp = min(puntaje1, puntaje2)
    diferencia = round(pg - pp, 2)

    resumen = (
        f"{ganador.nombre} ({ganador.raza}) venció a {perdedor.nombre} ({perdedor.raza}) "
        f"con un puntaje de {pg} vs {pp} (diferencia: {diferencia} pts). "
        f"Sus stats decisivos — Fuerza: {ganador.fuerza}, Agilidad: {ganador.agilidad}, "
        f"Magia: {ganador.magia}, Conocimiento: {ganador.conocimiento} — "
        f"le dieron la ventaja estratégica sobre su rival."
    )

    resultado = ResultadoBatalla(
        ganador=PersonajeOut.model_validate(ganador),
        perdedor=PersonajeOut.model_validate(perdedor),
        puntaje_ganador=pg,
        puntaje_perdedor=pp,
        diferencia=diferencia,
        resumen=resumen,
    )

    return ApiResponse(
        success=True,
        message=f"Batalla completada: '{ganador.nombre}' derrota a '{perdedor.nombre}'.",
        data=resultado,
    )
