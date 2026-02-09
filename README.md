# FALA.AI Backend

Minimal FastAPI backend scaffold using uv for dependency management, async SQLAlchemy with PostgreSQL, and JWT-secured CRUD for `usuarios_admin`.

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (`pip install uv`)
- PostgreSQL 15+
- Optional: Docker & Docker Compose v2

## Development Environment

### Option A – Using Docker (recommended for isolated setup)

1. Ensure Docker Desktop/Engine and Compose v2 are available.
2. Copy the example env file for container usage: `cp .env.example .env` (root) and optional `cp .env docker/.env` if you prefer overriding inside the compose stack.
3. Start the stack with hot reload via `./run.sh` (runs `docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build`).
4. API is reachable at `http://localhost:8001`; Postgres listens on `localhost:5433` with credentials from `.env`.
5. To stop the stack, hit `Ctrl+C` or from the `docker/` folder run `docker compose -f docker-compose.yml -f docker-compose.dev.yml down`.
6. Alembic commands can be executed inside the API container, e.g. `docker compose exec api uv run alembic revision -m "add table"` or `docker compose exec api uv run alembic upgrade head`.
	- The dev compose override sets `UV_PROJECT_ENVIRONMENT=/app/.venv-docker`, preventing conflicts with local virtual environments.

### Option B – Native (when Docker is unavailable)

1. Install Python 3.11+, uv, and PostgreSQL locally.
2. Copy `.env.example` to `.env` and adjust DB host/port if you run Postgres locally.
3. Run `./scripts/bootstrap.sh` to install packages and apply migrations.
4. (Optional) Seed an admin: `uv run python scripts/create_admin.py <email> "<Nome>" "<Senha>"`.
5. (Optional) If you want the database via Docker only, execute `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d db` and stop with the same command plus `down`.
6. Start the dev server with `uv run uvicorn app.main:app --reload` (defaults to `http://127.0.0.1:8000`).
7. Use `uv run pytest` for tests and the scripts in `scripts/` to manage migrations.

## Local Setup

```bash
# FALA.AI Backend

Backend em FastAPI com SQLAlchemy assíncrono, autenticação JWT e foco inicial no CRUD de usuários administradores.

## Requisitos

- Python 3.11 ou superior
- [uv](https://github.com/astral-sh/uv) (`pip install uv`)
- PostgreSQL 15 ou superior
- Docker + Docker Compose v2 (opcional, recomendado)

## Preparação inicial

```bash
git clone <repo>
cd falaai
cp .env.example .env
./scripts/bootstrap.sh
```

O script `bootstrap.sh` instala dependências (`uv sync`) e aplica a migration inicial.

## Ambiente de desenvolvimento

### Docker (recomendado)

1. Garanta Docker Engine/Compose v2 instalados.
2. Ajuste `.env` se necessário (por padrão já aponta `DATABASE_HOST=db`).
3. Rode `./run.sh` na raiz do projeto.
	- Internamente executa `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up --build` com hot reload.
4. API em `http://localhost:8001`; Postgres disponível em `localhost:5433` (usuário `falaai`, senha `falaaidevpass`).
5. Para encerrar, `Ctrl+C` ou `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml down` dentro de `docker/`.
6. Migrations dentro do container: `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml exec api uv run alembic <comando>`.

### Execução nativa

1. Instale Python 3.11+, uv e PostgreSQL local.
2. Copie `.env.example` para `.env` e ajuste `DATABASE_HOST`/`DATABASE_PORT` para o seu banco.
3. Execute `./scripts/bootstrap.sh`.
4. (Opcional) Suba apenas o banco via Docker: `docker compose -f docker/docker-compose.yml -f docker/docker-compose.dev.yml up -d db`.
5. Inicie o servidor: `uv run uvicorn app.main:app --reload` (porta padrão `8000`).
6. Testes: `uv run pytest`.
7. Migrations locais: `uv run alembic <comando>`.

## Criar usuário administrador

```bash
uv run python scripts/create_admin.py admin@example.com "Admin" "senha"
```

Depois autentique em `POST /api/v1/auth/login` para gerar o token.

## Alembic e migrations

### Conceito

Alembic versiona o schema: cada arquivo em `alembic/versions` define como aplicar (`upgrade`) ou desfazer (`downgrade`) uma alteração estrutural.

### Comandos frequentes

- `uv run alembic current` — status atual da base.
- `uv run alembic revision -m "descricao"` — criação manual de revisão.
- `uv run alembic revision --autogenerate -m "descricao"` — geração automática a partir dos modelos.
- `uv run alembic upgrade head` — aplica todas as pendências.
- `uv run alembic downgrade -1` — volta uma revisão (apenas em desenvolvimento).
- Dentro do Docker, utilize `docker compose ... exec api uv run alembic ...`.
- Doc oficial: https://alembic.sqlalchemy.org/en/latest/

### Como adicionar uma nova tabela

1. **Model**: crie a classe em `app/models/`, herdando de `Base`, definindo `__tablename__`, colunas (`mapped_column`) e constraints necessárias.
2. **Registrar**: importe o modelo em `app/models/__init__.py` para que o metadata enxergue a tabela.
3. **Schemas/CRUD** (se exposto via API): adicione DTOs em `app/schemas/` e operações em `app/crud/`.
4. **Migration**: com o banco ativo, execute `uv run alembic revision --autogenerate -m "descricao"` e revise o arquivo gerado em `alembic/versions` (ajuste índices, defaults, colunas obrigatórias manualmente quando necessário).
5. **Aplicar**: `uv run alembic upgrade head` (ou o comando equivalente dentro do container) para materializar a tabela.
6. **Verificar**: use `psql` (`\d`) ou `inspect(engine.sync_engine).get_table_names()` e adicione testes.

### Rolling back

- `uv run alembic downgrade -1` desfaz a última alteração em ambientes de desenvolvimento.
- Após corrigir, rode `uv run alembic upgrade head` novamente.
- Em produção, combine com a equipe antes de aplicar downgrades.

### Checklist rápido

1. Modelo em `app/models` + import no `__init__`.
2. Schemas em `app/schemas`.
3. CRUD/serviços em `app/crud`.
4. Rotas e dependências em `app/api`.
5. Migration gerada e revisada em `alembic/versions`.
6. `uv run alembic upgrade head` executado.
7. Testes (`uv run pytest`) atualizados.
8. Documentação ajustada.

## Scripts úteis

- `scripts/bootstrap.sh` — instala dependências e roda migrations.
- `scripts/migrate.sh` — aplica `alembic upgrade head`.
- `scripts/create_admin.py` — cria um administrador via CLI.
- `run.sh` — sobe o stack Docker com hot reload.

## Testes

```bash
uv run pytest
```

## Endpoints úteis

- Documentação Swagger: `http://localhost:8000/docs` (nativo) ou `http://localhost:8001/docs` (Docker).
- Health check: `GET /api/v1/health`.
