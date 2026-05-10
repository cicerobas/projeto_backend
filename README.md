# projeto_backend

API REST desenvolvida para o projeto *Raízes do Nordeste*. Utiliza o framework Fastapi, PostgreSQL como banco de dados, SQLModel como ORM e autenticação via JWT.

---

## Requisitos

| Ferramenta | Versão mínima |
|---|---|
| Docker | 24+ |
| Docker Compose | 2.20+ |

> Não é necessário instalar Python, uv ou PostgreSQL localmente — tudo roda dentro dos containers.

Se preferir rodar **sem Docker**, você precisará de:
- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- PostgreSQL 14+

---

## 1. Clonar o repositório

```bash
git clone https://github.com/cicerobas/projeto_backend
cd projeto_backend
```

---

## 2. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha os valores:

```bash
cp .env.example .env
```

Abra o `.env` e preencha os campos obrigatórios:

```env
# Segurança JWT
SECRET_KEY=sua_chave_secreta_aqui    # Gere uma chave com: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Usuário administrador inicial
ADMIN_EMAIL=admin@email.com
ADMIN_PASSWORD=sua_senha_aqui

# Banco de dados
DB_USER=postgres
DB_PASSWORD=sua_senha_do_banco
DB_HOST=db                              # use "db" para Docker; "localhost" para rodar local
DB_PORT=5432
DB_NAME=db_projeto
```

---

## 3. Instalar dependências

### Com Docker (recomendado)

As dependências são instaladas automaticamente ao fazer o build. Pule para o passo 4.

### Sem Docker

```bash
uv sync
```

---

## 4. Criar o banco e executar migrations

### Com Docker

O banco é criado automaticamente pelo container `db`. As tabelas são criadas na inicialização da aplicação.

### Sem Docker

Certifique-se de que o PostgreSQL está rodando e o banco `db_projeto` existe:

```bash
psql -U postgres -c "CREATE DATABASE db_projeto;"
```

As tabelas são criadas automaticamente ao iniciar a API.

---

## 5. Iniciar a API

### Com Docker (recomendado)

```bash
docker compose up --build
```

Para rodar em segundo plano:

```bash
docker compose up --build -d
```

Para parar:

```bash
docker compose down
```

### Sem Docker

```bash
uv run fastapi run app/main.py --port 8000
```

---

## 6. Acessar a documentação

Com a API no ar, acesse:

| Interface | URL |
|---|---|
| Swagger UI | [http://localhost:8000/docs](http://localhost:8000/docs) |
| ReDoc | [http://localhost:8000/redoc](http://localhost:8000/redoc) |

---
## 7. Testes

Importe o arquivo `Testes.postman_collection.json` no Postman e execute via **Collection Runner**.

**Antes de rodar:**

1. Preencha admin_password nas variáveis da coleção
    
2. Execute a pasta 'Setup' primeiro para popular os dados necessários
    
3. Execute as pastas A, B, C, D na ordem

As demais rotas podem ser acessadas e testadas em [http://localhost:8000/docs](http://localhost:8000/docs).

## Estrutura do projeto

```
projeto_backend/
├── app/              # Código-fonte
├── .env.example      # Modelo de variáveis de ambiente
├── pyproject.toml    # Dependências e configurações do projeto
├── uv.lock           # Lockfile do uv
├── Dockerfile
└── docker-compose.yml
```