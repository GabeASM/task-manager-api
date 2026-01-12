# Task Manager API

[![CI/CD](https://github.com/TU_USUARIO/task-manager-api/actions/workflows/ci.yml/badge.svg)](https://github.com/TU_USUARIO/task-manager-api/actions)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Django 6.0](https://img.shields.io/badge/django-6.0-green.svg)](https://www.djangoproject.com/)
[![DRF 3.16](https://img.shields.io/badge/DRF-3.16-red.svg)](https://www.django-rest-framework.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> API REST profesional para gestión de tareas construida con Django REST Framework, PostgreSQL, autenticación JWT y CI/CD con GitHub Actions.

## 🚀 Características

- ✅ **CRUD completo** de tareas con autenticación
- ✅ **Autenticación JWT** con refresh tokens
- ✅ **Filtrado y búsqueda** de tareas
- ✅ **Endpoints personalizados** (pendientes, completadas, estadísticas)
- ✅ **Documentación automática** con Swagger/ReDoc
- ✅ **Tests comprehensivos** con pytest (>90% cobertura)
- ✅ **CI/CD** con GitHub Actions
- ✅ **Docker** y Docker Compose
- ✅ **PostgreSQL** como base de datos

## 📋 Requisitos previos

- Python 3.12+
- PostgreSQL 15+ (o Docker)
- Git

## 🛠️ Instalación

### Opción 1: Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/task-manager-api.git
cd task-manager-api

# Copiar variables de entorno
cp .env.example .env

# Levantar servicios
docker-compose up --build

# Crear superusuario
docker-compose exec web python manage.py createsuperuser
```

La API estará disponible en `http://localhost:8000`

### Opción 2: Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/task-manager-api.git
cd task-manager-api

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements-dev.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

## 📚 Documentación de la API

Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva:

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **ReDoc**: http://localhost:8000/api/schema/redoc/
- **Admin Django**: http://localhost:8000/admin/

## 🔐 Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación.

### Obtener tokens

```bash
POST /api/token/
Content-Type: application/json

{
  "username": "tu_usuario",
  "password": "tu_contraseña"
}
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Usar el token

Incluye el token de acceso en el header `Authorization`:

```bash
GET /api/tasks/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Refrescar token

```bash
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 🔧 Endpoints principales

### Usuarios

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/users/register/` | Registrar nuevo usuario |
| GET/PUT | `/api/users/profile/` | Ver/actualizar perfil |
| PUT | `/api/users/change-password/` | Cambiar contraseña |
| GET | `/api/users/me/` | Info del usuario actual |

### Tareas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/tasks/` | Listar tareas |
| POST | `/api/tasks/` | Crear tarea |
| GET | `/api/tasks/{id}/` | Ver detalle |
| PUT/PATCH | `/api/tasks/{id}/` | Actualizar tarea |
| DELETE | `/api/tasks/{id}/` | Eliminar tarea |
| GET | `/api/tasks/pending/` | Tareas pendientes |
| GET | `/api/tasks/completed/` | Tareas completadas |
| POST | `/api/tasks/{id}/complete/` | Marcar como completada |
| GET | `/api/tasks/stats/` | Estadísticas |

## 🧪 Tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov

# Solo tests de una app
pytest tasks/
pytest users/

# Ver reporte de cobertura en HTML
pytest --cov --cov-report=html
# Abrir htmlcov/index.html
```

## 🎨 Linting y formateo

```bash
# Formatear código con black
black .

# Ordenar imports con isort
isort .

# Verificar estilo con flake8
flake8 .
```

## 🐳 Docker

```bash
# Construir y levantar servicios
docker-compose up --build

# Solo base de datos
docker-compose up -d db

# Ver logs
docker-compose logs -f web

# Ejecutar comandos
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Detener servicios
docker-compose down

# Eliminar volúmenes
docker-compose down -v
```

## 📊 Estructura del proyecto

```
task-manager-api/
├── config/                 # Configuración de Django
│   ├── settings.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── tasks/                  # App de tareas
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── tests/
├── users/                  # App de usuarios
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests/
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions
├── .env.example           # Variables de entorno de ejemplo
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── pytest.ini
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## 🚀 CI/CD

El proyecto incluye un pipeline de CI/CD con GitHub Actions que ejecuta:

1. **Tests** con pytest
2. **Linting** con flake8
3. **Formateo** con black
4. **Cobertura** de código
5. **Build** de Docker
6. **Análisis de seguridad**

El pipeline se ejecuta automáticamente en cada push a `main` o `develop` y en cada pull request.

## 🔒 Variables de entorno

Configura las siguientes variables en tu archivo `.env`:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=taskmanager
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

## 📝 Licencia

Este proyecto es de código abierto bajo la licencia MIT.

## 👤 Autor

**Tu Nombre**
- GitHub: [@tu_usuario](https://github.com/tu_usuario)
- LinkedIn: [Tu LinkedIn](https://linkedin.com/in/tu-perfil)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Soporte

Si tienes alguna pregunta o problema, por favor abre un issue en GitHub.