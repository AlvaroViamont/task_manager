# 📝 Task Manager API

Una API RESTful desarrollada con **FastAPI** y **SQLAlchemy** para gestionar tareas. Permite operaciones CRUD completas, filtrado por estado, ordenamiento dinámico y actualización parcial del estado de las tareas. Ideal como base para aplicaciones tipo to-do list o gestores de productividad.

---

## 📦 Estructura del Proyecto

# 📝 Task Manager API

Una API RESTful desarrollada con **FastAPI** y **SQLAlchemy** para gestionar tareas. Incluye funcionalidades como roles, usuarios, autenticación, autorización, y migraciones con Alembic. Arquitectura basada en servicios y separación de responsabilidades.

---

## 📦 Estructura del Proyecto (Arquitectura por Servicios)

```
project/
│
├── app/
│   ├── main.py               # Punto de entrada FastAPI con lifespan
│   ├── core/                 # Configuración, seguridad y utilidades
│   │   ├── config.py         # Variables de entorno (Settings)
│   │   ├── security.py       # Lógica de JWT y password hashing
│   │   └── dependencies.py   # Dependencias comunes (get_db, get_current_user)
│   ├── database/
│   │   ├── session.py        # Engine y sesión de SQLAlchemy
│   │   ├── base.py           # Declaración global de Base
│   ├── models/               # Modelos ORM
│   │   ├── __init__.py
│   │   ├── task.py
│   │   ├── user.py
│   │   ├── role.py
│   │   └── association.py
│   ├── schemas/              # Esquemas de Pydantic
│   │   ├── task.py
│   │   ├── user.py
│   │   └── role.py
│   ├── services/             # Lógica de negocio (por recurso)
│   │   ├── task_service.py
│   │   ├── user_service.py
│   │   └── auth_service.py
│   └── api/                  # Rutas separadas por recurso
│       ├── deps.py           # Dependencias comunes de API
│       ├── routes/
│       │   ├── auth.py
│       │   ├── tasks.py
│       │   ├── users.py
│       │   └── roles.py
│       └── router.py         # Incluye todos los routers
├── alembic/                  # Migraciones con Alembic
│   ├── versions/
│   └── env.py
├── .env                     # Variables de entorno
├── requirements.txt         # Dependencias
├── alembic.ini
└── README.md
```

---

## 🔐 Módulo de Autenticación y Autorización

- Contraseñas seguras con `passlib`
- Tokens JWT con `python-jose`
- Endpoints:
  - `POST /auth/login` → genera token
  - `GET /me` → usuario actual

**Autorización por rol:**
- Decoradores y dependencias (`get_current_user`, `get_current_admin`, etc.)
- Filtro en endpoints según permisos

---

## 🔧 Módulo de Servicios

Servicios desacoplados acceden a la base de datos a través de sesiones:

```python
# task_service.py
from app.models import Task

def get_tasks(db, user_id):
    return db.query(Task).filter(Task.user_id == user_id).all()
```

---

## 📦 Migraciones con Alembic

1. Inicializar Alembic:
```bash
alembic init alembic
```
2. Configurar `env.py` para importar `Base.metadata`
3. Generar migraciones:
```bash
alembic revision --autogenerate -m "add user and role"
```
4. Aplicar:
```bash
alembic upgrade head
```

---

## 🛡️ Roles sugeridos

| Rol     | Permisos                                          |
|---------|---------------------------------------------------|
| user    | CRUD de sus propias tareas                        |
| manager | Leer tareas de su equipo, asignar responsables    |
| admin   | Control total del sistema, gestión de usuarios    |

---

## 🚀 Instrucciones para Ejecutar el Proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/task-api.git
cd task-api
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo `.env` en la raíz del proyecto con este contenido:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TODO_DB=nombre_de_tu_bd
TODO_USER=usuario
TODO_PASSWORD=contraseña

JWT_SECRET=clave_secreta
ALGORITHM=HS256
```

### 5. Crear las tablas en la base de datos

Podés crear las tablas ejecutando un script temporal o agregando en tu código:

```python
# script_init_db.py
from app.database import engine
from app.models import Base

Base.metadata.create_all(bind=engine)
```

Luego lo ejecutás:

```bash
python script_init_db.py
```

### 6. Ejecutar el servidor

```bash
uvicorn main:app --reload
```

La API estará disponible en:

- 📍 `http://127.0.0.1:8000`
- 📘 Documentación interactiva: `http://127.0.0.1:8000/docs`
- 📕 Redoc: `http://127.0.0.1:8000/redoc`

---

## 📌 Funcionalidades del Proyecto

### Tareas

- ✅ Crear una tarea
- 📋 Listar todas las tareas
- 🔍 Filtrar por estado (`pending`, `in_progress`, `completed`)
- ⬆️⬇️ Ordenar por campos (`title`, `status`, `due_date`)
- 🧾 Obtener tarea por ID
- 🛠️ Actualizar campos de una tarea
- 🔄 Cambiar solo el estado de una tarea
- ❌ Eliminar una tarea

---

## 🧱 Tecnologías Utilizadas

| Tecnología | Rol                               |
| ---------- | --------------------------------- |
| FastAPI    | Framework principal               |
| SQLAlchemy | ORM para base de datos            |
| Pydantic   | Validación de datos               |
| PostgreSQL | Motor de base de datos relacional |
| Uvicorn    | Servidor ASGI para FastAPI        |
| dotenv     | Manejo de variables de entorno    |

---

## 🛡️ Seguridad

- Soporte preparado para autenticación con **JWT**.
- Las claves `JWT_SECRET` y `ALGORITHM` ya están integradas en el sistema de configuración.
- Se recomienda usar variables de entorno y nunca subir `.env` al repositorio (`.gitignore` debe incluirlo).

---

## ✅ Recomendaciones

- Usar Alembic si el proyecto requiere migraciones estructuradas.
- Integrar autenticación JWT si querés controlar acceso por usuario.
- Agregar pruebas unitarias con `pytest` para asegurar la calidad del código.

---

## 🥪 Pruebas (opcional)

Para agregar pruebas automáticas:

```bash
pip install pytest httpx
```

Y crear un archivo `test_main.py` con:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
```

---

## 📄 Licencia

Este proyecto está bajo licencia [MIT](https://opensource.org/licenses/MIT).

---

## ✨ Autor

Desarrollado por **Alvaro Viamont Rico** 🚀