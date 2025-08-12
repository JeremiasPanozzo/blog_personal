from flask import Blueprint, render_template, request, redirect, url_for, session
from . import get_db_connection
from datetime import datetime

bp = Blueprint("routes", __name__)

@bp.route("/")
def index():
    return render_template("index.html")

@bp.route("/contacto")
def contacto():
    return render_template("contacto.html")

@bp.route("/blogs")
def blogs():
    conn = get_db_connection()

    posts = conn.execute("""SELECT posts.titulo, posts.contenido, posts.fecha_creacion, categorias.nombre AS categoria
        FROM posts LEFT JOIN categorias ON posts.id = categorias.id
        ORDER BY posts.fecha_creacion DESC""").fetchall()
    
    conn.close()
    return render_template("blog.html", posts=posts)

@bp.route("/buscar", methods=["GET"])
def buscar():
    query = request.args.get("q", "").strip()
    conn = get_db_connection()

    if not query:
        # Si no envían búsqueda, mostramos todos o mensaje vacío
        posts = conn.execute("""
            SELECT posts.*, categories.name AS category
            FROM posts
            LEFT JOIN categories ON posts.category_id = categories.id
            ORDER BY date_created DESC
        """).fetchall()
    else:
        # Búsqueda segura con LIKE y parámetros
        like_query = f"%{query}%"
        posts = conn.execute("""
            SELECT posts.*, categories.name AS category
            FROM posts
            LEFT JOIN categories ON posts.category_id = categories.id
            WHERE posts.title LIKE ? OR posts.content LIKE ?
            ORDER BY date_created DESC
        """, (like_query, like_query)).fetchall()

    conn.close()

    return render_template("blog.html", posts=posts, search=query)

@bp.app_errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404