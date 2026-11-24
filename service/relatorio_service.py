from sqlalchemy import func
from sqlalchemy.orm import Session
from model.evento import Evento
from model.participante import Participante
from model.inscricao import Inscricao


def relatorio_ocupacao_eventos(db: Session):
    resultados = (
        db.query(
            Evento.id,
            Evento.titulo,
            Evento.capacidade,
            func.count(Inscricao.id).label("total_inscritos"),
        )
        .outerjoin(Inscricao, Evento.id == Inscricao.evento_id)
        .group_by(Evento.id)
        .all()
    )

    relatorio = []
    for evento_id, titulo, capacidade, total_inscritos in resultados:
        vagas_disponiveis = max(capacidade - total_inscritos, 0)
        percentual_ocupacao = (
            round((total_inscritos / capacidade) * 100, 2) if capacidade > 0 else 0.0
        )
        relatorio.append(
            {
                "evento_id": evento_id,
                "titulo": titulo,
                "capacidade": capacidade,
                "total_inscritos": total_inscritos,
                "vagas_disponiveis": vagas_disponiveis,
                "percentual_ocupacao": percentual_ocupacao,
            }
        )
    return relatorio


def relatorio_eventos_por_categoria(db: Session):
    subquery_inscricoes = (
        db.query(
            Inscricao.evento_id.label("evento_id"),
            func.count(Inscricao.id).label("qtd_inscricoes"),
        )
        .group_by(Inscricao.evento_id)
        .subquery()
    )

    resultados = (
        db.query(
            Evento.categoria,
            func.count(Evento.id).label("total_eventos"),
            func.coalesce(func.sum(Evento.capacidade), 0).label("capacidade_total"),
            func.coalesce(func.sum(subquery_inscricoes.c.qtd_inscricoes), 0).label(
                "total_inscricoes"
            ),
        )
        .outerjoin(subquery_inscricoes, Evento.id == subquery_inscricoes.c.evento_id)
        .group_by(Evento.categoria)
        .all()
    )

    return [
        {
            "categoria": categoria,
            "total_eventos": total_eventos,
            "capacidade_total": int(capacidade_total),
            "total_inscricoes": int(total_inscricoes),
        }
        for categoria, total_eventos, capacidade_total, total_inscricoes in resultados
    ]


def relatorio_participacao_por_curso(db: Session):
    resultados = (
        db.query(
            Participante.curso,
            func.count(func.distinct(Participante.id)).label("total_participantes"),
            func.count(Inscricao.id).label("total_inscricoes"),
        )
        .outerjoin(Inscricao, Participante.id == Inscricao.participante_id)
        .group_by(Participante.curso)
        .all()
    )

    return [
        {
            "curso": curso,
            "total_participantes": total_participantes,
            "total_inscricoes": total_inscricoes,
        }
        for curso, total_participantes, total_inscricoes in resultados
    ]
