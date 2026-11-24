from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from model.usuario import Usuario
from schema.usuario_schema import UsuarioCreate
from security.security import gerar_hash_senha


def criar_usuario(db: Session, dados: UsuarioCreate) -> Usuario:
    existente = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if existente:
        raise HTTPException(
            status_code=409,
            detail="Já existe um usuário cadastrado com este e-mail.",
        )

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=gerar_hash_senha(dados.senha),
        perfil="usuario",
    )
    try:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Já existe um usuário cadastrado com este e-mail.",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Erro ao cadastrar usuário no banco de dados.",
        )
