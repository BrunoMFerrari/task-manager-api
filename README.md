 # Task Manager API (Python)

API REST desenvolvida em Python para gerenciamento de tarefas.

Este projeto foi construído como evolução de um sistema gerenciador de tarefas no terminal, com o objetivo de aprender conceitos fundamentais de backend, como criação de APIs, manipulação de banco de dados e organização de código em aplicações reais.

⸻

🚀 Funcionalidades
	•	Criar tarefas
	•	Listar todas as tarefas
	•	Buscar tarefa por título
	•	Atualizar tarefas
	•	Deletar tarefas
	•	Marcar tarefa como concluída
	•	Filtro por prioridade e por status

⸻

🧠 Tecnologias utilizadas
	•	Python
	•	FastAPI
	•	Uvicorn
	•	Pydantic
	•	SQLAlchemy

⸻

📂 Estrutura do projeto

app/
	•	main.py → inicialização da API e rotas
	•	models.py → modelos do banco de dados
	•	schemas.py → validação de dados com Pydantic
	•	auth_routes.py -> rotas de autenticação
	•	tasks_routes.py -> rotas de gerenciamento de tarefas
  •	dependencies.py -> funcionalidades do sistema
