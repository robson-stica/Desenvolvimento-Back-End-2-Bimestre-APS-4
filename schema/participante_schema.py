import re
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ParticipanteBase(BaseModel):
    nome: str = Field(description="Nome do participante")
    email: str = Field(description="E-mail do participante")
    curso: str = Field(description="Curso do participante")

    @field_validator("nome", "curso")
    @classmethod
    def nao_pode_ser_vazio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O campo não pode ser vazio.")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        v = v.strip()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("E-mail inválido.")
        return v


class ParticipanteCreate(ParticipanteBase):
    pass


class ParticipanteUpdate(ParticipanteBase):
    pass


class ParticipanteResponse(ParticipanteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
