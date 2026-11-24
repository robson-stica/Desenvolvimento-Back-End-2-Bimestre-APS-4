from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from model.usuario import Usuario
from schema.usuario_schema import LoginRequest
from security.security import verificar_senha, criar_token_acesso


def autenticar_usuario(db: Session, dados: LoginRequest) -> dict:
    usuario = db.query(Usuario).filter(Usuario.email == dados.email.strip()).first()
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha inválidos.",
        )

    token = criar_token_acesso(usuario)
    return {"access_token": token, "token_type": "bearer"}
