import os
from fastapi import FastAPI
from database import Base, SessionLocal, engine
from model import evento, participante, inscricao, usuario
from model.usuario import Usuario
from security.security import gerar_hash_senha
from controller import (
    auth_controller,
    evento_controller,
    inscricao_controller,
    participante_controller,
    relatorio_controller,
    usuario_controller,
)

Base.metadata.create_all(bind=engine)


def criar_admin_inicial():
    db = SessionLocal()
    try:
        admin_email = os.getenv("ADMIN_EMAIL", "admin@eventos.com")
        admin_nome = os.getenv("ADMIN_NOME", "Administrador")
        admin_senha = os.getenv("ADMIN_SENHA", "admin123")
        existente = db.query(Usuario).filter(Usuario.email == admin_email).first()
        if not existente:
            admin = Usuario(
                nome=admin_nome,
                email=admin_email,
                senha_hash=gerar_hash_senha(admin_senha),
                perfil="administrador",
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()


criar_admin_inicial()

app = FastAPI(
    title="API de Eventos Acadêmicos - APS 4",
    description="API RESTful com persistência em SQLite, autenticação JWT e controle de acesso por perfil.",
    version="2.0.0",
)

app.include_router(usuario_controller.router)
app.include_router(auth_controller.router)
app.include_router(evento_controller.router)
app.include_router(participante_controller.router)
app.include_router(inscricao_controller.router)
app.include_router(relatorio_controller.router)
