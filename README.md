# API de Eventos Acadêmicos — APS 4

API RESTful desenvolvida com Python, FastAPI, SQLite, SQLAlchemy ORM, Argon2 (`pwdlib`) e tokens JWT (`PyJWT`), evoluindo a APS 3 com autenticação e autorização baseada em perfis.

## Estrutura do Projeto

```text
APS4/
├── main.py
├── database.py
├── .env.example
├── controller/
│   ├── auth_controller.py
│   ├── usuario_controller.py
│   ├── evento_controller.py
│   ├── participante_controller.py
│   ├── inscricao_controller.py
│   └── relatorio_controller.py
├── model/
│   ├── usuario.py
│   ├── evento.py
│   ├── participante.py
│   └── inscricao.py
├── schema/
│   ├── usuario_schema.py
│   ├── evento_schema.py
│   ├── participante_schema.py
│   └── inscricao_schema.py
├── service/
│   ├── auth_service.py
│   ├── usuario_service.py
│   ├── evento_service.py
│   ├── participante_service.py
│   ├── inscricao_service.py
│   └── relatorio_service.py
├── security/
│   └── security.py
├── requirements.txt
└── README.md
```

## Configuração da Chave Secreta e Variáveis de Ambiente

Copie `.env.example` para `.env` e defina sua chave secreta antes de executar em produção:
```env
SECRET_KEY=sua-chave-secreta-aqui
ADMIN_NOME=Administrador
ADMIN_EMAIL=admin@eventos.com
ADMIN_SENHA=admin123
```
Na inicialização da aplicação, caso ainda não exista o usuário administrador configurado em `ADMIN_EMAIL`, ele é criado automaticamente no banco SQLite com perfil `administrador`.

## Instalação e Execução

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Execute o servidor:
   ```bash
   uvicorn main:app --reload
   ```
3. Acesse o Swagger em `http://127.0.0.1:8000/docs`.

## Perfis e Permissões

- **Rotas públicas**: `POST /usuarios`, `POST /auth/login`, `GET /eventos`, `GET /eventos/{id}`.
- **Usuário autenticado (`usuario` e `administrador`)**:
  - `GET /auth/me`
  - `POST /participantes`, `GET /participantes`, `GET /participantes/{id}`, `PUT /participantes/{id}`
  - `POST /eventos/{evento_id}/inscricoes/{participante_id}`, `GET /eventos/{evento_id}/inscricoes`
- **Somente Administrador (`administrador`)**:
  - `POST /eventos`, `PUT /eventos/{id}`, `DELETE /eventos/{id}`
  - `DELETE /participantes/{id}`
  - `GET /relatorios/eventos/ocupacao`, `GET /relatorios/eventos/categorias`, `GET /relatorios/participantes/cursos`

## Como Cadastrar Usuários e Obter Token

1. Envie `POST /usuarios` com `nome`, `email` e `senha` (mínimo 6 caracteres). Todo usuário cadastrado pela rota recebe o perfil `usuario`.
2. Envie `POST /auth/login` com `email` e `senha`.
3. Copie o `access_token` retornado e envie no cabeçalho `Authorization: Bearer <token>` (ou clique em **Authorize** no Swagger `/docs`).

## Como Reproduzir os Testes

1. Cadastre um usuário comum via `POST /usuarios` e faça login em `POST /auth/login`.
2. Teste `GET /auth/me` com o token válido.
3. Tente acessar uma rota protegida sem token ou com token inválido (esperado `401 Unauthorized`).
4. Tente criar um evento em `POST /eventos` usando o token do usuário comum (esperado `403 Forbidden`).
5. Faça login com o administrador inicial, crie eventos, cadastre participantes, realize inscrições e consulte os relatórios em `/relatorios/...`.
