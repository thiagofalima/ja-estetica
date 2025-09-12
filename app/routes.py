from flask import Blueprint, render_template, request, flash, redirect, url_for

from passlib.hash import pbkdf2_sha256
from uuid import uuid4
from datetime import datetime
from app.forms import RegisterForm, LoginForm
from app.models import Client

pages = Blueprint("pages", __name__, template_folder="templates")


@pages.route("/")
def home():
    return render_template("home.html", title="JA - Estética")


@pages.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for("pages.home"))

    return render_template("login.html", title="JA - Estética | Login", form=form)


@pages.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        cliente = Client(
            _id=uuid4().hex,
            name=form.name.data,
            birth_date=(form.birth_date.data).isoformat(),
            email=form.email.data,
            password=pbkdf2_sha256.hash(form.password.data),
            register_date=datetime.now().isoformat(),
        )

        print(cliente)

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for("pages.login"))

    return render_template("register.html", title="JA - Estética | Cadastro", form=form)
