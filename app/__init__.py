from flask import Flask
import sqlite3
import os
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from datetime import timedelta
from flask_wtf import CSRFProtect
from .extensions import limiter

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'database.db')
load_dotenv()

csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    app.secret_key = os.getenv("SECRET_KEY")
    app.config["WTF_CSRF_ENABLED"] = True
    #Duracion de la sesion
    app.permanent_session_lifetime = timedelta(minutes=30)

    # Cookies y headers más seguros (en dev, si no usas HTTPS, puedes desactivar SECURE temporalmente)
    app.config.update(
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SECURE=False,      # Requiere HTTPS
        SESSION_COOKIE_SAMESITE='Lax',
        PERMANENT_SESSION_LIFETIME=1800
    )

    csrf.init_app(app)
    limiter.init_app(app)

    from . import routes, auth 

    app.register_blueprint(auth.bp)
    app.register_blueprint(routes.bp) 

    init_db()

    return app

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            contenido TEXT NOT NULL,
            categoria_id INTEGER,
            fecha_creacion TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
    ''')

    admin_pw = os.getenv("ADMIN_PASSWORD", "")
    hashed_pw = generate_password_hash(admin_pw)  
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn 