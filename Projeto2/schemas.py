
from pydantic import BaseModel
from enum import Enum


# 13-Valores que podem ser atribuidos a variável prioridade 
class PrioridadeEnum(str, Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAIXA = "BAIXA"


# 15.2-Valores possíveis para status
class StatusEnum(str, Enum):
    PENDENTE = "PENDENTE"
    COMPLETA = "COMPLETA"


# 7-Esquema para a criação de um novo usuário
class SchemaUsuario(BaseModel):
    nome: str
    email: str
    senha: str

    class Config:
        from_attributes = True


# 9-Esquema para a criação de uma nova tarefa
class SchemaTarefa(BaseModel):
    titulo: str
    prioridade: PrioridadeEnum # 13-Adicionando prioridade

    class Config:
        from_attributes = True

    
# 10-Esquema para login na conta
class SchemaLogin(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True