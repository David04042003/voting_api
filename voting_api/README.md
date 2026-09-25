# Voting API

API RESTful desarrollada con **FastAPI**, **PostgreSQL**, **SQLAlchemy** y autenticación **JWT** para gestionar un sistema de votaciones.

Permite registrar votantes y candidatos, emitir votos, validar que cada votante vote una sola vez, y consultar estadísticas de resultados.

## Tecnologías

- Python 3
- FastAPI
- PostgreSQL
- SQLAlchemy (ORM)
- Pydantic (validación de datos)
- JWT (python-jose) para autenticación
- Uvicorn (servidor)
- Swagger / OpenAPI (documentación automática)

## Estructura del proyecto

```
voting_api/
├── app/
│   ├── main.py              # Punto de entrada de la app
│   ├── database.py          # Conexión a PostgreSQL
│   ├── core/
│   │   └── security.py      # Creación y validación de JWT
│   ├── auth/
│   │   └── router.py        # Endpoint de login
│   ├── voters/               # Modelo, schema, servicio y endpoints de votantes
│   ├── candidates/           # Modelo, schema, servicio y endpoints de candidatos
│   └── votes/                # Modelo, schema, servicio y endpoints de votos
├── requirements.txt
├── .env.example
└── README.md
```

## Instalación y ejecución local

1. Clonar el repositorio y entrar a la carpeta:
   ```bash
   git clone <url-del-repo>
   cd voting_api
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

## Autenticación

Todos los endpoints de `voters`, `candidates` y `votes` requieren un token JWT.

Usuario fijo de prueba:
- **username:** `admin`
- **password:** `admin123`

### Obtener un token (curl)

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Respuesta:
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

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
