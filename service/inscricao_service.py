from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from model.evento import Evento
from model.participante import Participante
from model.inscricao import Inscricao


def inscrever_participante(db: Session, evento_id: int, participante_id: int):
    evento = db.get(Evento, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")

    participante = db.get(Participante, participante_id)
    if not participante:
        raise HTTPException(status_code=404, detail="Participante não encontrado.")

    ja_inscrito = (
        db.query(Inscricao)
        .filter(
            Inscricao.evento_id == evento_id,
            Inscricao.participante_id == participante_id,
        )
        .first()
    )
    if ja_inscrito:
        raise HTTPException(
            status_code=409,
            detail="Participante já está inscrito neste evento.",
        )

    total_inscritos = db.query(Inscricao).filter(Inscricao.evento_id == evento_id).count()
    if total_inscritos >= evento.capacidade:
        raise HTTPException(
            status_code=409,
            detail="Não existem vagas disponíveis para este evento.",
        )

    inscricao = Inscricao(evento_id=evento_id, participante_id=participante_id)
    try:
        db.add(inscricao)
        db.commit()
        db.refresh(inscricao)
        return inscricao
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Participante já está inscrito neste evento.",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao registrar inscrição no banco de dados.",
        )


def listar_inscritos_evento(db: Session, evento_id: int):
    evento = db.get(Evento, evento_id)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")

    return [inscricao.participante for inscricao in evento.inscricoes]
