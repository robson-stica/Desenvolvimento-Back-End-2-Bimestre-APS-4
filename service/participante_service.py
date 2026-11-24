from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from model.participante import Participante
from schema.participante_schema import ParticipanteCreate, ParticipanteUpdate


def criar_participante(db: Session, dados: ParticipanteCreate):
    existente = db.query(Participante).filter(Participante.email == dados.email).first()
    if existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe um participante cadastrado com este e-mail.",
        )

    participante = Participante(**dados.model_dump())
    try:
        db.add(participante)
        db.commit()
        db.refresh(participante)
        return participante
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Já existe um participante cadastrado com este e-mail.",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao salvar participante no banco de dados.",
        )


def listar_participantes(db: Session):
    return db.query(Participante).all()


def buscar_participante_por_id(db: Session, participante_id: int):
    participante = db.get(Participante, participante_id)
    if not participante:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")
    return participante


def atualizar_participante(db: Session, participante_id: int, dados: ParticipanteUpdate):
    participante = buscar_participante_por_id(db, participante_id)

    existente = (
        db.query(Participante)
        .filter(Participante.email == dados.email, Participante.id != participante_id)
        .first()
    )
    if existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe um participante cadastrado com este e-mail.",
        )

    for campo, valor in dados.model_dump().items():
        setattr(participante, campo, valor)

    try:
        db.commit()
        db.refresh(participante)
        return participante
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Já existe um participante cadastrado com este e-mail.",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao atualizar participante no banco de dados.",
        )


def excluir_participante(db: Session, participante_id: int):
    participante = buscar_participante_por_id(db, participante_id)
    try:
        db.delete(participante)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao excluir participante no banco de dados.",
        )
