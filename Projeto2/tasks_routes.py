
from fastapi import APIRouter, HTTPException
from dependencies import new_session, search_token
from sqlalchemy.orm import Session
from fastapi import Depends
from models import Tarefa, Usuario
from schemas import SchemaTarefa, PrioridadeEnum, StatusEnum




# 3.1-Criando o roteador que abrigará todas as rotas de "/tasks"
tasks_router = APIRouter(prefix="/tasks", tags=["tasks"], dependencies=[Depends(search_token)]) #

# 3.2-Criando rota "/tasks/" experimental - JÁ USADA
#@tasks_router.get("/")
#async def tasks():
#    return {"mensagem": "Rota padrão criada com sucesso"}




# 9-Criando rota para criar novas tarefas
@tasks_router.post("/new_task")
async def new_task(nova_tarefa_schema: SchemaTarefa,
                    session: Session=Depends(new_session),
                    user: Usuario = Depends(search_token)
                    ):
    
    """
    Aqui você pode criar uma nova tarefa que será cadastrada ao seu usuário
    Prioridade deve ser: "ALTA", "MEDIA" ou "BAIXA", nesse formato
    """
    
    existe_tarefa = session.query(Tarefa).filter(Tarefa.titulo == nova_tarefa_schema.titulo and Tarefa.id_user == user.id_user).first()

    if existe_tarefa:
        raise HTTPException(status_code=400, detail="Essa tarefa já foi registrada")
    else:
        nova_tarefa = Tarefa(nova_tarefa_schema.titulo, user.id_user, nova_tarefa_schema.prioridade)
        session.add(nova_tarefa)
        session.commit()
        return {"mensagem": f"Tarefa {nova_tarefa.titulo} cadastrada com sucesso | PRIORIDADE : {nova_tarefa.prioridade}"}




# 12.1-Rota para concluir tarefa
@tasks_router.post("/finish_task/{id_task}")
async def finish_task(id_task: int,
                      session: Session = Depends(new_session),
                      user: Usuario = Depends(search_token)
                      ):
    
    """
    Aqui você pode concluir uma de suas tarefas
    """
    
    existe_tarefa = session.query(Tarefa).filter(Tarefa.id_task == id_task).first()

    if not existe_tarefa:
        raise HTTPException(status_code=400, detail="Tarefa não existe")
    if existe_tarefa.id_user != user.id_user:
        raise HTTPException(status_code=401, detail="Você não pode alterar essa tarefa")
    
    existe_tarefa.status = "COMPLETA"
    session.commit()
    return {
        "mensagem": f"Tarefa de Id {existe_tarefa.id_task} completa com sucesso!",
        "task": existe_tarefa
    }

# 12.2-Rota para listar suas tarefas
@tasks_router.get("/list_tasks")
async def list_tasks(user: Usuario = Depends(search_token)):
    
    """
    Aqui você pode listar todas as suas tarefas
    """

    return {
        "tasks": user.tarefas
    }

# 12.3-Deletar tarefa 
@tasks_router.post("/delete_task/{id_task}")
async def delete_task(id_task: int,
                      session: Session = Depends(new_session),
                      user: Usuario = Depends(search_token)
                      ):
    
    """
    Aqui você pode apagar uma de suas tarefas do banco de dados
    """
    
    existe_tarefa = session.query(Tarefa).filter(Tarefa.id_task == id_task).first()

    if not existe_tarefa:
        raise HTTPException(status_code=400, detail="Tarefa não encontrada")
    if existe_tarefa.id_user != user.id_user:
        raise HTTPException(status_code=401, detail="Você não pode deletar essa tarefa")
    
    # Deletar o pedido do banco de dados
    session.delete(existe_tarefa)
    session.commit()
    return {
        "mensagem": "Tarefa removida com sucesso",
        "tarefas": user.tarefas
    }




# 14-Buscar tarefas específicas
@tasks_router.get("/search_task")
async def search_task(titulo: str,
                      session: Session = Depends(new_session),
                      user: Usuario = Depends(search_token)
                      ):
    """
    Essa função busca tarefas específicas conectadas ao seu usuário
    """

    existe_tarefa = session.query(Tarefa).filter(Tarefa.titulo == titulo.strip() and Tarefa.id_user == user.id_user).first()

    if not existe_tarefa:
        raise HTTPException(status_code=400, detail="Tarefa não existe")
    
    return {
        "tarefa": existe_tarefa
    }




# 15.1-Adicionar filtro de pesquisa por prioridade
@tasks_router.get("/search_task/filter_priority")
async def filter_priority(prioridade_desejada: PrioridadeEnum,
                          session: Session = Depends(new_session),
                          user: Usuario = Depends(search_token)
                          ):
    
    """
    Busca tarefas com determinada prioridade que estajam conectadas à sua conta
    """

    lista_tarefas = session.query(Tarefa).filter(Tarefa.prioridade == prioridade_desejada and Tarefa.id_user == user.id_user).all()

    
    if not lista_tarefas:
        raise HTTPException(status_code=400, detail="Nenhuma tarefa com essa prioridade encontrada")

    return {
        "lista_tarefas": lista_tarefas
    }


# 15.2-Adicionar filtro de pesquisa por status
@tasks_router.get("/search_task/filter_status")
async def filter_status(status_desejado: StatusEnum,
                          session: Session = Depends(new_session),
                          user: Usuario = Depends(search_token)
                          ):
    
    """
    Busca tarefas com determinado status que estajam conectadas à sua conta
    """

    lista_tarefas = session.query(Tarefa).filter(Tarefa.status == status_desejado and Tarefa.id_user == user.id_user).all()

    if not lista_tarefas:
        raise HTTPException(status_code=400, detail="Nenhuma tarefa com esse status encontrada")

    return {
        "lista_tarefas": lista_tarefas
    }