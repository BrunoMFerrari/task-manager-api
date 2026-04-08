
from fastapi import APIRouter, HTTPException, Depends
from dependencies import new_session, search_token
from sqlalchemy.orm import Session
from schemas import SchemaUsuario, SchemaLogin
from models import Usuario
from main import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_STANDART_EXPIRATION_MINUTES, bcrypt_context
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm




# 10.1-Criando função para verificar o login
def verify_login(email, senha, session):
    # Vai filtrar a coluna "email" da tabela "Usuario". Caso exista retorna o usuario em si, caso não exista retorna False
    existe_usuario = session.query(Usuario).filter(Usuario.email==email).first()

    if not existe_usuario:
        return False
    
    # Caso usuário exista mas a senha passada no login seja != da senha cadastrada no "existe_usuario"
    elif not bcrypt_context.verify(senha, existe_usuario.senha):
        return False
    
    # Caso exista o usuário e a senha cadastrada esteja correta, retornamos o usuário desejado
    else:
        return existe_usuario

# 10.2.1-Função para automatizar a criação de tokens
def new_token(id_user, # Id do usuário que fez o login
              token_expiration=timedelta(minutes=ACCESS_TOKEN_STANDART_EXPIRATION_MINUTES) # Tempo de expiração do token a ser criado
              ):
    
    exp = datetime.now(timezone.utc) + token_expiration # Definindo data e hora de expiração
    token_info = {
        "sub": str(id_user),
        "exp": exp
    }
    encoded_jwt = jwt.encode(token_info, SECRET_KEY, ALGORITHM) # Cripitografando o token
    return encoded_jwt




# 3.1-Criando o roteador que abrigará todas as rotas de "/auth"
auth_router = APIRouter(prefix="/auth", tags=["auth"])

# 3.2-Criando rota "/auth/" experimental - JÁ FOI USADA
#@auth_router.get("/")
#async def auth():
#    """
#    Essa é uma rota experimental
#    """
#    return {"mensagem": "Rota padrão criada com sucesso"}




# 8-Criando uma rota para criação de um novo usuário
@auth_router.post("/new_user") # Tipo post pois ela vai postar algo para o meu sistema
async def new_user(novo_usuario_schema: SchemaUsuario, # Recebendo os parâmetros de um new_user através do SchemaUsuario
                    session: Session=Depends(new_session) # Recebendo a sessão
                    ):
    
    """
    Aqui você pode cadastrar sua conta no banco de dados do sistema
    """

    # 8.1-Buscando se o email desejado já está no banco de dados
    existe_email = session.query(Usuario).filter(Usuario.email==novo_usuario_schema.email).first() # Filtrando a tabela "Usuario" por emails iguais
 
    # 8.2-Mostrando mensagem de erro caso exista
    if existe_email:
        raise HTTPException(status_code=400, detail="E-mail digitado já foi cadastrado")
    
    # 8.3-Se não existir, adicionando o novo usuário ao banco efetivamente
    else:
        senha_cripitografada = bcrypt_context.hash(novo_usuario_schema.senha) # Usando o meu cripitografador de senhas

        novo_usuario = Usuario(novo_usuario_schema.nome, novo_usuario_schema.email, senha_cripitografada)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário {novo_usuario_schema.nome} cadastrado com sucesso"}




# 10-Criando rota de login
@auth_router.post("/login")
async def login(login_schema: SchemaLogin, # Informações para login
                session: Session = Depends(new_session)
                ):
    
    """
    Aqui você pode fazer login na sua conta
    """
    
    # 10.1-Verificar se o email já está cadastrado e se a senha digitada está correta
    existe_usuario = verify_login(login_schema.email, login_schema.senha, session)
    if not existe_usuario:
        raise HTTPException(status_code=401, detail="Verifique se e-mail digitado foi cadastrado ou se a está senha correta")

    # 10.2-Caso positivo, criar token de acesso(access_token) e um token de restauração(refresh_token)
    else:
        # 10.2.1-Criar função "new_token" para automatizar a criação de tokens
    
        access_token = new_token(existe_usuario.id_user)
        refresh_token = new_token(existe_usuario.id_user, timedelta(days=7))
        return {"access_token": access_token, # "access_token" - acesso as funções do usuário dentro do site - curto prazo
                "refresh_token": refresh_token, # "refresh_token" - automatizar a criação de um access_token - medio prazo
                "token_type": "Bearer"
                }


# 10-Rota de login alternativa usando o refresh token
@auth_router.get("/login_with_refresh_token")
async def login_with_refresh_token(usuario: Usuario = Depends(search_token)): # Função para reconhecer a qual usuário o token passado pertence

    """
    Essa função serve para acessar o sistema sem precisar logar novamente
    """

    # Criando um novo access token para o usuário requisitado
    access_token = new_token(usuario.id_user)

    return {"access_token": access_token,
            "token_type": "Bearer"
            }




# 11-Criando uma rota de login através do formulario
@auth_router.post("/login_form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(),
                     session: Session = Depends(new_session)
                     ):
    
    """
    Essa função serve apenas para que o formulário do FastAPI funcione e deixe os testes mais rápidos
    """
    
    existe_usuario = verify_login(dados_formulario.username, dados_formulario.password, session)
    
    if not existe_usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou senha inválida")
    else:
        access_token = new_token(existe_usuario.id_user)
        refresh_token = new_token(existe_usuario.id_user, timedelta(days=7))
        return {"access_token": access_token, "token_type": "Bearer"}
