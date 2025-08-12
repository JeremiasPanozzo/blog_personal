from flask import Blueprint, render_template, request, redirect, url_for, session
from . import get_db_connection
from werkzeug.security import check_password_hash

bp = Blueprint("auth", __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()

        user = conn.execute("SELECT * FROM usuarios WHERE nombre_usuario = ?", (username,)).fetchone()

        conn.close()

        if user and check_password_hash(user["password_hash"], password):
            session.permanent = True
            
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("routes.index"))
        else:
            return render_template("login.html", error="Credenciales inválidas")

    return render_template("login.html")

@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("routes.index"))