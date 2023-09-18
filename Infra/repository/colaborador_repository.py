from Infra.configs.connection import DBConnectionHandler
from Infra.entities.colaborador import Colaborador

class ColaboradorRepository:
    def select (self):
        with DBConnectionHandler () as db:
            data = db.session.query(Colaborador).all()
            return data 
    def insert(self,matricula,nome,email,senha):
         with DBConnectionHandler () as db:
             data_insert = Colaborador(matricula=matricula,nome= nome,email=email,senha=senha)
             db.session.add(data_insert)
             db.session.commit()
             
    def delete(self,matricula):
         with DBConnectionHandler () as db:
             db.session.query(Colaborador).filter (Colaborador.matricula==matricula).delete() #deletar um por um
             #(Colaborador.matricula.in_(["6","7","8","9"])).delete() #deletar varios
             db.session.commit()
    def update(self,matricula,nome,email,senha):
         with DBConnectionHandler () as db:
             db.session.query (Colaborador).filter(Colaborador.matricula == matricula,nome== nome,email==email,senha==senha).update({"matricula","nome","email","senha"})
             db.session.commit()      