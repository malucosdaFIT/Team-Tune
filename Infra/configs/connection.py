from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:
    def __init__(self) -> None:
        self.___connection_string = "mysql+pymysql://root:vinicius123!@localhost:3306/teamtune"
        self.__engine = self.__create_databese_engine()
        self.session = None

    def __create_databese_engine(self):
        engine = create_engine(self.___connection_string)
        return engine
    def get_engine(self):
        return self.__engine
    def __enter__(self):
        session_make =sessionmaker(bind=self.__engine)
        self.session=session_make()
        return self
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.session.close()