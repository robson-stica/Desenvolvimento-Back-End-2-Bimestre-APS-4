from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from schema.inscricao_schema import InscricaoResponse
from schema.participante_schema import ParticipanteResponse
from security.security import get_current_user
from service import inscricao_service

router = APIRouter(prefix="/eventos", tags=["Inscrições"])


@router.post(
    "/{evento_id}/inscricoes/{participante_id}",
    response_model=InscricaoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Inscrever participante em um evento",
)
def inscrever(
    evento_id: int,
    participante_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return inscricao_service.inscrever_participante(db, evento_id, participante_id)


@router.get(
    "/{evento_id}/inscricoes",
    response_model=list[ParticipanteResponse],
    summary="Listar participantes inscritos em um evento",
)
def listar_inscritos(
    evento_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return inscricao_service.listar_inscritos_evento(db, evento_id)
