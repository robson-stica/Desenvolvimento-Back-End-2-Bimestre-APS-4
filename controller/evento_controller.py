from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from schema.evento_schema import EventoCreate, EventoUpdate, EventoResponse
from security.security import require_admin
from service import evento_service

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.post("", response_model=EventoResponse, status_code=status.HTTP_201_CREATED, summary="Cadastrar evento (Admin)")
def criar_evento(
    dados: EventoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return evento_service.criar_evento(db, dados)


@router.get("", response_model=list[EventoResponse], summary="Listar todos os eventos")
def listar_eventos(db: Session = Depends(get_db)):
    return evento_service.listar_eventos(db)


@router.get("/{evento_id}", response_model=EventoResponse, summary="Consultar evento por ID")
def buscar_evento(evento_id: int, db: Session = Depends(get_db)):
    return evento_service.buscar_evento_por_id(db, evento_id)


@router.put("/{evento_id}", response_model=EventoResponse, summary="Atualizar evento (Admin)")
def atualizar_evento(
    evento_id: int,
    dados: EventoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return evento_service.atualizar_evento(db, evento_id, dados)


@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Excluir evento (Admin)")
def excluir_evento(
    evento_id: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    evento_service.excluir_evento(db, evento_id)
