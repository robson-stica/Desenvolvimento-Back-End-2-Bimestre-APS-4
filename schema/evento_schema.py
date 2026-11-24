from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


class EventoBase(BaseModel):
    titulo: str = Field(description="Título do evento")
    descricao: str = Field(description="Descrição do evento")
    data: str = Field(description="Data do evento no formato YYYY-MM-DD")
    horario: str = Field(description="Horário do evento no formato HH:MM")
    local: str = Field(description="Local de realização")
    capacidade: int = Field(gt=0, description="Capacidade máxima de participantes")
    categoria: str = Field(description="Categoria do evento")

    @field_validator("titulo", "descricao", "local", "categoria")
    @classmethod
    def nao_pode_ser_vazio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O campo não pode ser vazio.")
        return v.strip()

    @field_validator("data")
    @classmethod
    def validar_data(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Data inválida. Use o formato YYYY-MM-DD.")
        return v

    @field_validator("horario")
    @classmethod
    def validar_horario(cls, v: str) -> str:
        try:
            datetime.strptime(v, "%H:%M")
        except ValueError:
            raise ValueError("Horário inválido. Use o formato HH:MM.")
        return v


class EventoCreate(EventoBase):
    pass


class EventoUpdate(EventoBase):
    pass


class EventoResponse(EventoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
