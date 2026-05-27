# Backend ILAR – Orquestador de Servicios

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)
![Docker](https://img.shields.io/badge/Docker-24%2B-2496ED)

## 📌 Descripción del Proyecto

Este proyecto corresponde al backend de un **orquestador de servicios** desarrollado con **FastAPI**, diseñado para centralizar y administrar operaciones relacionadas con usuarios y futuros módulos de negocio.

Un **orquestador** es una aplicación que coordina múltiples servicios o módulos dentro de una plataforma. En este caso, el backend busca servir como núcleo de comunicación entre diferentes componentes de un sistema turístico/logístico.

Actualmente el proyecto incluye:

* Gestión de usuarios.
* Registro y autenticación mediante JWT.
* Base de datos PostgreSQL.
* Redis como servicio auxiliar/cache.
* Migraciones con Alembic.
* Arquitectura modular preparada para expansión.

### 🔄 Estado del Proyecto

| Módulo                 | Estado           |
| ---------------------- | ---------------- |
| Usuarios               | ✅ Funcional      |
| Autenticación JWT      | ✅ Funcional      |
| Reservas               | 🚧 En desarrollo |
| Transporte / TMS       | 🚧 En desarrollo |
| Integraciones externas | 🚧 Pendiente     |

> ⚠️ Algunos módulos aún están en construcción. Actualmente el backend funcional principal es el módulo de usuarios y autenticación.

---

# 🚀 Inicio Rápido (Local)

## 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd backend_Ilar-master
```

---

## 2. Crear el archivo `.env`

El proyecto utiliza variables de entorno para manejar configuraciones sensibles.

⚠️ **IMPORTANTE:**

* Nunca subas el archivo `.env` al repositorio.
* Asegúrate de incluir `.env` en `.gitignore`.
* Las claves de producción deben ser diferentes a las de desarrollo.

Ejemplo mínimo:

```env
DB_user=postgres
DB_password=post
DB_host=localhost
DB_port=5432
DB_name=develop

DATABASE_URL=postgresql+asyncpg://postgres:post@db:5432/develop
DATABASE_URL_SYNC=postgresql+psycopg2://postgres:post@localhost:5432/develop

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_URL=redis://redis:6379/0

APP_NAME=GDS_Backend
DEBUG=True
API_V1_STR=/api/v1

SECRET_KEY=tu_clave_super_segura

LOG_LEVEL=info
JSON_LOGS=True
```

---

## 3. Levantar los servicios con Docker

```bash
docker compose up --build
```

Esto iniciará:

| Servicio        | Puerto |
| --------------- | ------ |
| FastAPI Backend | 8000   |
| PostgreSQL      | 5432   |
| Redis           | 6379   |

---

## 4. Verificar que el backend esté funcionando

Abrir en el navegador:

```txt
http://localhost:8000/docs
```

Swagger UI mostrará toda la documentación interactiva de la API.

También puedes usar:

```txt
http://localhost:8000/redoc
```

---

# 🧰 Requisitos de Software

## Requisitos mínimos

| Herramienta    | Versión recomendada |
| -------------- | ------------------- |
| Python         | 3.12+               |
| Docker         | 24+                 |
| Docker Compose | 2.20+               |
| PostgreSQL     | 16                  |
| Redis          | 7+                  |
| Git            | Última estable      |

---

# 🏗️ Arquitectura General

```txt
Cliente Frontend
       │
       ▼
 FastAPI Backend
       │
 ├── PostgreSQL
 └── Redis
```

### Tecnologías principales

* FastAPI
* SQLAlchemy Async
* Alembic
* PostgreSQL
* Redis
* JWT Authentication
* Structlog
* Docker

---

# 📂 Estructura del Proyecto

```txt
backend_Ilar-master/
│
├── src/
│   ├── main.py
│   ├── database.py
│   ├── security.py
│   └── Modulos/
│       └── Usuario/
│           ├── Usuario_router.py
│           ├── Usuario_service.py
│           ├── Usuario_modelo.py
│           └── Usuario_schema.py
│
├── migrations/
├── docker-compose.yml
├── alembic.ini
├── pyproject.toml
└── .env
```

---

# 🔐 Autenticación

La autenticación se realiza mediante **JWT Bearer Token**.

## Flujo de autenticación

1. Registrar usuario.
2. Hacer login.
3. Obtener `access_token`.
4. Enviar el token en el header:

```http
Authorization: Bearer TU_TOKEN
```

---

# 📘 Guía de la API

## Swagger

```txt
http://localhost:8000/docs
```

## ReDoc

```txt
http://localhost:8000/redoc
```

---

## 👤 Registro de Usuario

### Endpoint

```http
POST /usuarios/registro
```

### Body

```json
{
  "nombre": "Juan",
  "correo": "juan@email.com",
  "password": "123456"
}
```

---

## 🔑 Login

### Endpoint

```http
POST /usuarios/login
```

### Tipo de contenido

```txt
application/x-www-form-urlencoded
```

### Parámetros

| Campo    | Descripción      |
| -------- | ---------------- |
| username | Correo o usuario |
| password | Contraseña       |

### Respuesta esperada

```json
{
  "access_token": "TOKEN_JWT",
  "token_type": "bearer"
}
```

---

## 👥 Obtener usuarios

```http
GET /usuarios/all
```

---

## 👤 Obtener usuario por ID

```http
GET /usuarios/{usuario_id}
```

---

## ✏️ Actualizar usuario

```http
PUT /usuarios/{usuario_id}
```

---

## 🗑️ Eliminar usuario

```http
DELETE /usuarios/{usuario_id}
```

---

# ⚙️ Variables de Entorno

| Variable          | Descripción                    |
| ----------------- | ------------------------------ |
| DB_user           | Usuario de PostgreSQL          |
| DB_password       | Contraseña de PostgreSQL       |
| DB_host           | Host de PostgreSQL             |
| DB_port           | Puerto de PostgreSQL           |
| DB_name           | Nombre de la base de datos     |
| DATABASE_URL      | URL async usada por SQLAlchemy |
| DATABASE_URL_SYNC | URL sync usada por Alembic     |
| REDIS_HOST        | Host de Redis                  |
| REDIS_PORT        | Puerto de Redis                |
| REDIS_URL         | URL completa de Redis          |
| APP_NAME          | Nombre de la aplicación        |
| DEBUG             | Habilita modo debug            |
| API_V1_STR        | Prefijo base de API            |
| SECRET_KEY        | Clave usada para firmar JWT    |
| LOG_LEVEL         | Nivel de logs                  |
| JSON_LOGS         | Habilita logs JSON             |

---

# 🗄️ Migraciones de Base de Datos

El proyecto utiliza **Alembic** para controlar versiones de la base de datos.

## Crear una migración

```bash
alembic revision --autogenerate -m "descripcion"
```

## Aplicar migraciones

```bash
alembic upgrade head
```

## Revertir última migración

```bash
alembic downgrade -1
```

---

# 🧪 Ejecución sin Docker

## 1. Crear entorno virtual

```bash
python -m venv venv
```

## 2. Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Instalar dependencias

```bash
pip install -e .
```

---

## 4. Ejecutar migraciones

```bash
alembic upgrade head
```

---

## 5. Ejecutar el servidor

```bash
uvicorn src.main:app --reload
```

---

# 🛡️ Seguridad

## Recomendaciones

* Nunca compartir el archivo `.env`.
* Cambiar `SECRET_KEY` en producción.
* No usar credenciales por defecto fuera de entornos locales.
* Restringir CORS en producción.
* Activar HTTPS detrás de un reverse proxy.

---

# 🧑‍💻 Información para Frontend

El frontend puede autenticarse usando:

```http
POST /usuarios/login
```

La respuesta devolverá un JWT:

```json
{
  "access_token": "TOKEN",
  "token_type": "bearer"
}
```

Luego el token debe enviarse así:

```http
Authorization: Bearer TOKEN
```

La documentación interactiva disponible en `/docs` permite probar endpoints directamente.

---

# 🐳 Docker Compose

Servicios definidos actualmente:

* PostgreSQL 16
* Redis
* FastAPI Backend

El backend ejecuta automáticamente:

```bash
alembic upgrade head
```

antes de iniciar el servidor.

---

# 📌 Problemas Conocidos

* Algunos módulos aún no están implementados.
* La autenticación todavía no protege todos los endpoints.
* CORS está abierto para desarrollo.
* El proyecto aún no tiene pipeline de CI/CD.

---

# 📈 Mejoras Futuras

* Integración completa de reservas.
* Integración de transporte/logística.
* Roles y permisos avanzados.
* Tests automatizados.
* Integración con servicios externos.
* Despliegue cloud.

---

# 👥 Equipo

Proyecto desarrollado para fines académicos y de integración de servicios.

---

# ✅ Checklist Técnica

| Validación                                    | Estado |
| --------------------------------------------- | ------ |
| ¿Se puede levantar desde cero?                | ✅ Sí   |
| ¿Las variables de entorno están documentadas? | ✅ Sí   |
| ¿Hay instrucciones de migración?              | ✅ Sí   |
| ¿La autenticación está explicada?             | ✅ Sí   |
| ¿Se advierte sobre `.env`?                    | ✅ Sí   |
| ¿El frontend puede usar login fácilmente?     | ✅ Sí   |

---

# 📄 Licencia

Uso académico / interno.
