from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class Inscricao(Base):
    __tablename__ = "inscricoes"
    __table_args__ = (
        UniqueConstraint("evento_id", "participante_id", name="uq_evento_participante"),
    )

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)
    participante_id = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    data_inscricao = Column(DateTime, default=datetime.now, nullable=False)

    evento = relationship("Evento", back_populates="inscricoes")
    participante = relationship("Participante", back_populates="inscricoes")
