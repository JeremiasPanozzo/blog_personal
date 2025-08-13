# Blog Personal con Flask

Este es un proyecto de blog personal desarrollado en **Flask**.  
Está diseñado para que **solo el administrador** (usuario `admin`) pueda autenticarse y publicar entradas.  
Los visitantes pueden leer los posts, pero no registrarse ni iniciar sesión.

## Características

- **Panel de login** exclusivo para el administrador.
- **Sistema de sesiones** para el control de autenticación.
- **Gestión de posts** (creación solo por admin, lectura pública).
- **Página de error 404 personalizada** con estilos propios.s

## Tecnologías utilizadas

- **Python 3.x**
- **Flask** (framework web)
- **SQLite** (base de datos ligera)
- **Werkzeug** (para hashing de contraseñas)
- **HTML5 / CSS3** (con Jinja2 templates)
  
## Requerimientos del sistema
### Requerimientos funcionales
* 1.1 Roles del usuario
    * Administrador
        * Puede iniciar sesión en el sistema.
        * Puede publicar nuevos posts.
        * Puede acceder a un panel de control (Dashboard) para gestionar el contenido.
        * Puede cerrar sesión.
    * Visitante (usuario no autenticado)
        * Puede acceder y leer los posts publicados en la sección Blog.
        * Puede acceder a la sección Contacto.
        * Puede iniciar sesión (solo el administrador posee credenciales).

* 1.2 Navegacion
    * La barra de navegación debe mostrar diferentes opciones según el estado de autenticación:
    * Si el administrador está logueado: 
       * Mostrar botones/enlaces a Dashboard, Publicar, y Cerrar sesión.
       * Si no hay sesión iniciada: Mostrar botones/enlaces a Blog, Contacto, y Iniciar sesión.
