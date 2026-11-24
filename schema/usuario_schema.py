import re
from pydantic import BaseModel, ConfigDict, Field, field_validator


class UsuarioCreate(BaseModel):
    nome: str = Field(description="Nome completo do usuário")
    email: str = Field(description="E-mail do usuário")
    senha: str = Field(description="Senha do usuário (mínimo 6 caracteres)")

    model_config = ConfigDict(extra="forbid")

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O nome não pode ser vazio.")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("E-mail inválido.")
        return v

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if not v or not v.strip() or len(v) < 6:
            raise ValueError("A senha deve possuir pelo menos 6 caracteres.")
        return v


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: str
    senha: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
