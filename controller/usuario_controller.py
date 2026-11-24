from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from schema.usuario_schema import UsuarioCreate, UsuarioResponse
from service import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, summary="Cadastrar usuário")
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    return usuario_service.criar_usuario(db, dados)
