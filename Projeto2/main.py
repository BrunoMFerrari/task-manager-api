
# 0-Para rodar o código, executar isso no teminal: uvicorn main:app --reload
# Todas bibliotecas usadas no projeto:
# pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose[cryptography] python-dotenv python-multipart alembic
# pip uninstall bcrypt & pip install bcrypt==4.0.1

# 0.1-Importando bibliotecas
from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

# 0.2-Criando e importando arquivo ".env" para usar as variáveis privadas do meu sistema
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_STANDART_EXPIRATION_MINUTES = int(os.getenv("ACCESS_TOKEN_STANDART_EXPIRATION_MINUTES"))


# 1-Criando meu aplicativo
app = FastAPI() 


# 2-Criando o meu cripitografador de senhas e 10-Variável para a manipulação de tokens
# 2-Para isso você precisa criar a variável "SECRET_KEY = yOuRseCREtKey" no arquivo ".env" e depois copiar o código abaixo
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 10
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login_form")


# 3-Adicionando as rotas do meu app à {auth_routes & task_routes} e importando-as
from auth_routes import auth_router
from tasks_routes import tasks_router


# 4-Ativando rotas importadas
app.include_router(auth_router)
app.include_router(tasks_router)


# 5-Criando o banco de dados em "models.py"


# 6-Criando o arquivo "dependencies.py" para cuidar do gerenciamento das sessões de alteração do meu banco de dados


# 7-Criando o arquivo "schemas.py" para criar esquemas/padrões de recebimento de dados


# 8-Criando rota para criação de um novo usuário em "auth_routes.py"


# 9-Criando rota para criação de uma nova tarefa em "tasks_routes.py"


# 10-Criando uma rota de login em "auth.py"


# 11-Criando rota para permitir o uso do botão "Authorize" no meu_app/docs para facilitar os testes durante a programação


# 12-Criando rotas para concluir tarefa, listar suas tarefas e deletar tarefas


# 13-Adicionando prioridade nas tarefas


# 14-Mecanismo para buscar tarefa específica 


# 15-Adicionar filtro de pesquisa por prioridade e status