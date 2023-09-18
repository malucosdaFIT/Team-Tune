from Infra.configs.base import Base
from sqlalchemy import Column, String, Integer

class Colaborador(Base):
    __tablename__ = 'colaborador'

    matricula = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    
    def __repr__(self):
     return f"Colaboradores [matricula={self.matricula},nome={self.nome},email={self.email},senha={self.senha}]"
