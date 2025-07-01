# 📝 Task Manager API

Una API RESTful desarrollada con **FastAPI** y **SQLAlchemy** para gestionar tareas. Permite operaciones CRUD completas, filtrado por estado, ordenamiento dinámico y actualización parcial del estado de las tareas. Ideal como base para aplicaciones tipo to-do list o gestores de productividad.

---

## 📦 Estructura del Proyecto

```
project/
│
├── app/
│   ├── __init__.py
│   ├── routes.py            # Endpoints de la API
│   ├── models.py            # Modelos ORM con SQLAlchemy
│   ├── schemas.py           # Esquemas de Pydantic para validación y serialización
│   └── database.py          # Configuración del motor y sesión de la base de datos
│
├── config.py                # Clase Settings con carga de variables desde .env
├── main.py                  # Punto de entrada principal de la aplicación FastAPI
├── .env                     # Variables de entorno (NO debe subirse al repositorio)
└── requirements.txt         # Lista de dependencias del proyecto
```

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