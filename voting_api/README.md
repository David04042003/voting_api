# Voting API

API RESTful desarrollada con **FastAPI**, **PostgreSQL**, **SQLAlchemy** y autenticación **JWT** para gestionar un sistema de votaciones.

Permite registrar votantes y candidatos, emitir votos, validar que cada votante vote una sola vez, y consultar estadísticas de resultados.

## Tecnologías

- Python 3
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Pydantic (validación de datos)
- JWT para autenticación
- Uvicorn (servidor)
- Swagger / OpenAPI (documentación automática)

## Estructura del proyecto

```
text
voting_api/
│
├── app/
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── service.py
│   │
│   ├── candidates/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   └── service.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── security.py
│   │
│   ├── voters/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   └── service.py
│   │
│   ├── votes/
│   │   ├── __init__.py
│   │   ├── model.py
│   │   ├── router.py
│   │   ├── schema.py
│   │   └── service.py
│   │
│   ├── __init__.py
│   ├── database.py
│   └── main.py
│
├── venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```
## Database Script

```sql
CREATE TABLE voters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    has_voted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    party VARCHAR(100),
    votes INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    voter_id INTEGER NOT NULL UNIQUE,
    candidate_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vote_voter
        FOREIGN KEY (voter_id)
        REFERENCES voters(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_vote_candidate
        FOREIGN KEY (candidate_id)
        REFERENCES candidates(id)
        ON DELETE CASCADE
);
```
## Instalación y ejecución local

1. Clonar el repositorio y entrar a la carpeta:
   ```bash
   git clone https://github.com/YOUR_USERNAME/voting-api.git
   cd voting-api
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # En Windows: venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear una base de datos PostgreSQL vacía (por ejemplo `voting_db`).

5. Copiar `.env.example` a `.env` y completar tus credenciales:
   ```bash
   cp .env.example .env
   ```

6. Ejecutar el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

7. Abrir la documentación interactiva en:
   ```
   http://localhost:8000/docs
   ```

Las tablas se crean automáticamente al arrancar la aplicación.

## Environment Variables

Crea un archivo `.env` en la carpeta raíz y agrega la siguiente configuración:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=voting_db
DB_USER=postgres
DB_PASSWORD=your_password

SECRET_KEY=my_super_secret_key_123
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```


Sustituye `tu_contraseña` por tu contraseña de PostgreSQL.

Importante: el archivo `.env` no debe subirse a GitHub.

---

## Run the Project

Run the API with:

```bash
uvicorn app.main:app --reload
```

## Authentication


La API utiliza autenticación JWT para proteger los puntos finales principales.

### Login Credentials

```text
username: admin
password: admin123
```

### Login Endpoint

```http
POST /auth/login
```

En Swagger, haga clic en el botón **Autorizar** e ingrese:

```text
username: admin
password: admin123
```


Tras la autorización, se podrán utilizar los puntos finales protegidos.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/login` | Generate JWT access token |

---

### Voters

| Method | Endpoint | Description |
|---|---|---|
| POST | `/voters/` | Register a new voter |
| GET | `/voters/` | Get all voters with filtering and pagination |
| GET | `/voters/{voter_id}` | Get voter by ID |
| DELETE | `/voters/{voter_id}` | Delete voter |

---

### Candidates

| Method | Endpoint | Description |
|---|---|---|
| POST | `/candidates/` | Register a new candidate |
| GET | `/candidates/` | Get all candidates with filtering and pagination |
| GET | `/candidates/{candidate_id}` | Get candidate by ID |
| DELETE | `/candidates/{candidate_id}` | Delete candidate |

---

### Votes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/votes/` | Cast a vote |
| GET | `/votes/` | Get all votes |
| GET | `/votes/statistics` | Get voting statistics |

---

## Filtrado y paginación

Los puntos de acceso a las listas de votantes y candidatos admiten filtrado y paginación mediante parámetros de consulta.

---

### Voters Filtering and Pagination

Endpoint:

```http
GET /voters/
```

Parámetros de consulta disponibles:

| Parameter | Type | Description |
|---|---|---|
| skip | integer | Number of records to skip |
| limit | integer | Maximum number of records to return |
| name | string | Filter voters by name |
| email | string | Filter voters by email |
| has_voted | boolean | Filter voters by voting status |

Examples:

Usa ese token en el header `Authorization: Bearer <token>` para los demás endpoints.

## Ejemplos de uso

### Registrar un votante
```bash
curl -X POST "http://localhost:8000/voters/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Eric Dev", "email": "eric@test.com"}'
```

### Registrar un candidato
```bash
curl -X POST "http://localhost:8000/candidates/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana Gomez", "party": "Verde"}'
```

### Emitir un voto
```bash
curl -X POST "http://localhost:8000/votes/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"voter_id": 1, "candidate_id": 1}'
```

### Ver estadísticas
```bash
curl "http://localhost:8000/votes/statistics" \
  -H "Authorization: Bearer <token>"
```

Respuesta:
```json
{
  "total_votes": 1,
  "total_voters_who_voted": 1,
  "results": [
    {
      "candidate_id": 1,
      "candidate_name": "Ana Gomez",
      "party": "Verde",
      "votes": 1,
      "percentage": 100.0
    }
  ]
}
```

## Validaciones implementadas

- Un email de votante no puede repetirse.
- Una persona no puede estar registrada como votante y candidato a la vez (ni viceversa).
- Un votante no puede emitir más de un voto.
- Al votar, se actualiza automáticamente `has_voted` del votante y se incrementa `votes` del candidato.
- Todos los endpoints (excepto `/auth/login` y `/`) requieren un token JWT válido.

## Extras incluidos

- Autenticación con JWT.
- Filtrado y paginación en `GET /voters` (por `name`, `email`, `has_voted`) y `GET /candidates` (por `name`, `party`).
- Documentación automática con Swagger en `/docs`.
