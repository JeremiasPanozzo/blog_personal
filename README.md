# Blog Personal con Flask

Este es un proyecto de blog personal desarrollado en **Flask**.  
Está diseñado para que **solo el administrador** (usuario `admin`) pueda autenticarse y publicar entradas.  
Los visitantes pueden leer los posts, pero no registrarse ni iniciar sesión.

## Características

- **Panel de login** exclusivo para el administrador.
- **Sistema de sesiones** para el control de autenticación.
- **Gestión de posts** (creación solo por admin, lectura pública).
- **Página de error 404 personalizada** con estilos propios.


## Tecnologías utilizadas

- **Python 3.x**
- **Flask** (framework web)
- **SQLite** (base de datos ligera)
- **Werkzeug** (para hashing de contraseñas)
- **HTML5 / CSS3** (con Jinja2 templates)

## Estructura del proyecto
/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── auth.py
│   ├── templates/
│   │   ├── layout.html
│   │   ├── index.html
│   │   ├── blog.html
│   │   ├── login.html
│   │   ├── 404.html
│   ├── static/
│       ├── css/
│       │   ├── layout.css
│       │   ├── 404.css
│       ├── js/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
├── README.md
└── .env
