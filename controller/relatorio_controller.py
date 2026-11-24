from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from security.security import require_admin
from service import relatorio_service

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/eventos/ocupacao", summary="Relatório de ocupação dos eventos (Admin)")
def ocupacao_eventos(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return relatorio_service.relatorio_ocupacao_eventos(db)


@router.get("/eventos/categorias", summary="Relatório de eventos por categoria (Admin)")
def eventos_por_categoria(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return relatorio_service.relatorio_eventos_por_categoria(db)


@router.get("/participantes/cursos", summary="Relatório de participação por curso (Admin)")
def participacao_por_curso(
    db: Session = Depends(get_db),
    _: Usuario = Depends(require_admin),
):
    return relatorio_service.relatorio_participacao_por_curso(db)
