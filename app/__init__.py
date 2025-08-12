from flask import Flask
import sqlite3
import os
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
from datetime import timedelta

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'database.db')
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.secret_key = os.getenv("SECRET_KEY")
    app.config["WTF_CSRF_ENABLED"] = True
    #Duracion de la sesion
    app.permanent_session_lifetime = timedelta(minutes=30)

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
    
    c.execute("INSERT OR IGNORE INTO usuarios (nombre_usuario, password_hash) VALUES (?, ?)", ("jeremias", hashed_pw))
    c.execute("INSERT OR IGNORE INTO categorias (nombre) VALUES ('General'), ('Hacking'), ('Personal')")    
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn 