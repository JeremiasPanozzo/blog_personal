import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from . import get_db_connection
from werkzeug.security import check_password_hash
from .extensions import limiter
from functools import wraps
from flask import session, redirect, url_for

bp = Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in") or not session.get("is_admin"):
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute("SELECT * FROM usuarios WHERE nombre_usuario = ?", (username,)).fetchone()

        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session.permanent = True
            session["logged_in"] = True
            session["username"] = username
            session["is_admin"] = (username == os.getenv("ADMIN_USERNAME", "admin"))
            return redirect(url_for("routes.index"))
        else:
            return render_template("login.html", error="Credenciales inválidas")

    return render_template("login.html")

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect(url_for("routes.index"))
