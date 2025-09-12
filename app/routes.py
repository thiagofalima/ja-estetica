from flask import Blueprint, render_template, request, flash, redirect, url_for

from passlib.hash import pbkdf2_sha256
from uuid import uuid4
from datetime import datetime, date, time
from app.forms import RegisterForm, LoginForm, AppointmentForm
import time as tm
from app.models import Client, Appointment

pages = Blueprint("pages", __name__, template_folder="templates")


@pages.route("/")
def home():
    return render_template("home.html", title="JA - Estética")

@pages.route("/register/", methods=["GET", "POST"])
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

@pages.route("/login/", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        return redirect(url_for("pages.home"))

    if not form.validate_on_submit():
        flash("Usuário ou senha incorretos!", "danger")
        return redirect(url_for("pages.login"))

    return render_template("login.html", title="JA - Estética | Login", form=form)


@pages.route("/appointment/", methods=["GET", "POST"])
def appointment():

    form = AppointmentForm()

    if request.method == "POST" and form.validate_on_submit():
        # procedure = Appointment()

        if form.procedure_date.data < date.today():
            flash("A data do procedimento não pode ser no passado. Por favor, escolha uma data futura.", "danger")
            # Retorna o template sem validar, mostrando o alerta e mantendo o usuário na mesma página
            return render_template('appointment.html', form=form)
        
        elif form.procedure_time.data < time(8, 0) or form.procedure_time.data > time(17, 0):            
            flash("Nosso horário é das 08:00 às 17:00", "danger")
            # Retorna o template sem validar, mostrando o alerta e mantendo o usuário na mesma página
            return render_template('appointment.html', form=form)
        else:
            flash("Procedimento agendado com sucesso!", "success")
            return redirect(url_for("pages.home"))

    return render_template("appointment.html", title="JA - Estética | Agendamento", form=form)

