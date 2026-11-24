from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from schema.participante_schema import (
    ParticipanteCreate,
    ParticipanteUpdate,
    ParticipanteResponse,
)
from security.security import get_current_user, require_admin
from service import participante_service

router = APIRouter(prefix="/participantes", tags=["Participantes"])


@router.post("", response_model=ParticipanteResponse, status_code=status.HTTP_201_CREATED, summary="Cadastrar participante")
def criar_participante(
    dados: ParticipanteCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return participante_service.criar_participante(db, dados)


@router.get("", response_model=list[ParticipanteResponse], summary="Listar todos os participantes")
def listar_participantes(
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return participante_service.listar_participantes(db)


@router.get("/{participante_id}", response_model=ParticipanteResponse, summary="Consultar participante por ID")
def buscar_participante(
    participante_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return participante_service.buscar_participante_por_id(db, participante_id)


@router.put("/{participante_id}", response_model=ParticipanteResponse, summary="Atualizar participante")
def atualizar_participante(
    participante_id: int,
    dados: ParticipanteUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return participante_service.atualizar_participante(db, participante_id, dados)


@router.delete("/{participante_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir participante (Admin)")
def excluir_participante(
    participante_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    participante_service.excluir_participante(db, participante_id)
