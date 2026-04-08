
from models import db
from sqlalchemy.orm import sessionmaker, Session
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from models import Usuario




# 6-Função que quando chamada abrirá a sessão, fara as alterações desejadas e a finalizará
def new_session():
    try:
        Session = sessionmaker(bind=db) # Sessão aberta e conectada com o meu banco
        session = Session()
        yield session # Retorna a sessão para ser utilizada sem encerrar a execução da próximas linhas de código
    finally:
        session.close()




# 10-Função para reconhecer a qual usuário um "refresh_token" pertence
def search_token(refresh_token: str = Depends(oauth2_schema), 
                 session: Session = Depends(new_session)
                 ):
    # 10.1-Ver se ele corresponde ao usuário de login
    try:
        token_info = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM) # Decodando as informações do token
        id_user = int(token_info.get("sub")) # Pegando o "id_user" que estava armazenado no token
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado")
    
    # 10.2-Ver se existe um usuário com o id_user
    existe_usuario = session.query(Usuario).filter(Usuario.id_user==id_user).first()
    if not existe_usuario:
        raise HTTPException(status_code=401, detail="Usuário não existe")
    
    # 10.3-Retornar o usuário que o token corresponde
    else:
        return existe_usuario
