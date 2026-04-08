# Arquivo para testar a requisição - temporário

import requests

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzc1Njk3NDg5fQ.2OKXH9ksRqI0vgsg4QTCbPl1Zv3VL6sbyLxjm-BqRBs"
}

requisicao = requests.get("http://127.0.0.1:8000/auth/login_with_refresh_token", headers=headers)
print(requisicao)
print(requisicao.json())