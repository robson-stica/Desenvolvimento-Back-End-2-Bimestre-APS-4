from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from model.usuario import Usuario
from schema.usuario_schema import LoginRequest, TokenResponse, UsuarioResponse
from security.security import get_current_user
from service import auth_service

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponse, summary="Autenticar usuário e gerar token JWT")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.autenticar_usuario(db, dados)


@router.get("/me", response_model=UsuarioResponse, summary="Consultar dados do usuário autenticado")
def me(usuario_atual: Usuario = Depends(get_current_user)):
    return usuario_atual
