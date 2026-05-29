# SERENA UCatólica - Proyecto FastAPI + SQLite

SERENA es una aplicación académica para estudiantes de la Universidad Católica de Colombia. Su objetivo es acercar a estudiantes que están pasando por un momento psicológico difícil a tres herramientas básicas: chatbot, diario emocional y contacto con Bienestar.

## Estructura del proyecto

```text
SERENA_UCatolica_Modular/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── validators.py
├── auth.py
├── chatbot.py
├── email_service.py
├── requirements.txt
├── .env.example
├── routers/
│   ├── __init__.py
│   ├── pages.py
│   └── api.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── registro.html
│   ├── login.html
│   ├── dashboard.html
│   ├── chatbot.html
│   ├── diario.html
│   ├── bienestar.html
│   └── recuperar_clave.html
└── static/
    └── styles.css
```

## Cómo ejecutar el proyecto en PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m uvicorn main:app --reload
```

Luego abrir:

```text
http://127.0.0.1:8000
```

## Qué contiene según la rúbrica

- Coherencia con el proyecto inicial: mantiene la idea de apoyo emocional SERENA.
- Dominio del tema: usa FastAPI, rutas, modelos, validaciones, entorno virtual y SQLite.
- Estructura: el código está separado en archivos y carpetas.
- Métodos HTTP: usa GET, POST, PUT y DELETE en la API.
- Enrutamiento: usa rutas por recurso, por ejemplo `/api/usuarios/{usuario_id}`.
- Modelos: usa SQLModel para tablas y Pydantic para datos de entrada/salida.
- Validaciones: correo institucional, campos obligatorios, semestre, cédula y celular numéricos.
- Base de datos: usa SQLite con SQLModel.

## Correos del proyecto

Este proyecto maneja dos correos:

1. Correo SERENA: se usa para recuperación de contraseña.
2. Correo Bienestar SERENA: recibe solicitudes del apartado de Bienestar.

Para configurar los correos, copiar `.env.example` como `.env` y completar los datos reales.

## Nota académica

El sistema guarda las solicitudes en la base de datos aunque el correo SMTP no esté configurado. Esto permite mostrar el funcionamiento del proyecto en clase sin depender de un servidor de correo real.
