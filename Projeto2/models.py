
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey 
from sqlalchemy.orm import declarative_base, relationship

# 5.1-Criando o banco de dados em si
db = create_engine("sqlite:///banco.db")


# 5.2-Criando a base do banco de dados
Base = declarative_base()


# 5.3-Criar as tabelas/classes do meu banco
# 5.3.1-Usuário
class Usuario(Base):
    __tablename__ = "usuarios"

    # 5.3.1.1-Colunas da tabela "usuarios"
    id_user = Column("id_user", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String, nullable=False)
    tarefas = relationship("Tarefa", cascade="all, delete")

    # 5.3.1.2-Função __init__, atributos que devem ser passados na criação de um novo_usuario
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

# 5.3.2-Tarefa
class Tarefa(Base):
    __tablename__ = "tarefas"

    # 5.3.2.1-Clunas da tabela "tarefas"
    id_task = Column("id_tarefas", Integer, primary_key=True, autoincrement=True)
    titulo = Column("titulo", String, nullable=False)
    status = Column("status", String)
    prioridade = Column("prioridade", String) # 13-Adicionando prioridade
    id_user = Column("id_user", ForeignKey("usuarios.id_user"))

    # 5.3.2.2-Função __init__, atributos que devem ser passados na criação de uma nova_tarefa
    def __init__(self, titulo, id_user, prioridade, status="PENDENTE"):
        self.titulo = titulo
        self.id_user = id_user
        self.prioridade = prioridade
        self.status = status


# 5.4-Executa o código e realiza a criação efetivamente 
# 5.4.1-Enviar no cmd: { alembic init alembic } caso ainda não exista uma pasta alembic no seu projeto

# 5.4.2-Colocar o caminho "sqlite:///banco.db" no arquivo "alembic.ini" na variável "sqlalchemy.url"

# 5.4.3-Alterar no arquivo "/alembic/env.py" {
#   import sys
#   import os
#   sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#   &
#   from models import Base
#   target_metadata = Base.metadata
#   }

# 5.4.4-Digitar no prompt após qualquer alteração no banco de dados: { alembic revision --autogenerate -m "Nome da Alteração" }

# 5.4.5-Digitar no prompt { alembic upgrade head }
