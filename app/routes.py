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
        FROM posts LEFT JOIN categorias ON posts.categoria_id = categorias.id
        ORDER BY posts.fecha_creacion DESC""").fetchall()
    
    conn.close()
    return render_template("blog.html", posts=posts)

@bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@bp.route("/publicar" , methods=["GET", "POST"])
def publicar():
    with get_db_connection() as conn:

        if request.method == "POST":
            titulo = request.form.get("titulo")
            contenido = request.form.get("contenido")
            categoria_id = request.form.get("categoria")

            fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            conn.execute("INSERT INTO posts (titulo, contenido, categoria_id, fecha_creacion) VALUES (?, ?, ?, ?)", (titulo, contenido, categoria_id, fecha_creacion))
            conn.commit()

            return redirect(url_for("routes.index"))
    
        categorias = [dict(cat) for cat in conn.execute("SELECT id, nombre FROM categorias").fetchall()]
        return render_template("publicar.html", categorias=categorias)

@bp.app_errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404