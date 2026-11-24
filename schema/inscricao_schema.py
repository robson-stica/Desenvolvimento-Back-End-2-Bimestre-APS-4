from datetime import datetime
from pydantic import BaseModel, ConfigDict


class InscricaoResponse(BaseModel):
    id: int
    evento_id: int
    participante_id: int
    data_inscricao: datetime

    model_config = ConfigDict(from_attributes=True)
