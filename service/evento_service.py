from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from model.evento import Evento
from model.inscricao import Inscricao
from schema.evento_schema import EventoCreate, EventoUpdate


def criar_evento(db: Session, dados: EventoCreate):
    evento = Evento(**dados.model_dump())
    try:
        db.add(evento)
        db.commit()
        db.refresh(evento)
        return evento
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao salvar evento no banco de dados.")


def listar_eventos(db: Session):
    return db.query(Evento).all()


def buscar_evento_por_id(db: Session, evento_id: int):
    evento = db.get(Evento, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
    return evento


def atualizar_evento(db: Session, evento_id: int, dados: EventoUpdate):
    evento = buscar_evento_por_id(db, evento_id)
    total_inscritos = db.query(Inscricao).filter(Inscricao.evento_id == evento_id).count()
    if dados.capacidade < total_inscritos:
        raise HTTPException(
            status_code=400,
            detail="A capacidade não pode ser menor que a quantidade de participantes já inscritos.",
        )

    for campo, valor in dados.model_dump().items():
        setattr(evento, campo, valor)

    try:
        db.commit()
        db.refresh(evento)
        return evento
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao atualizar evento no banco de dados.")


def excluir_evento(db: Session, evento_id: int):
    evento = buscar_evento_por_id(db, evento_id)
    try:
        db.delete(evento)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao excluir evento no banco de dados.")
