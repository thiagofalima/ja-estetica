from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    redirect,
    url_for,
    session,
    current_app,
)
from dataclasses import asdict
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

    if session.get("email"):
        return redirect(url_for("pages.home"))

    form = RegisterForm()

    if form.validate_on_submit():
        if current_app.db.clients.find_one({"email": form.email.data}):
            flash("Usuário já cadastrado!", "danger")
            return redirect(url_for("pages.login"))
        else:
            cliente = Client(
                _id=uuid4().hex,
                name=form.name.data,
                birth_date=(form.birth_date.data).isoformat(),
                phone_number=form.phone_number.data,
                email=form.email.data,
                password=pbkdf2_sha256.hash(form.password.data),
                register_date=datetime.now().isoformat(),
            )

            current_app.db.clients.insert_one(asdict(cliente))

            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("pages.home"))

    return render_template("register.html", title="JA - Estética | Cadastro", form=form)


@pages.route("/login/", methods=["GET", "POST"])
def login():

    if session.get("email"):
        return redirect(url_for("pages.home"))

    form = LoginForm()

    if form.validate_on_submit():
        # DB verification
        cliente_data = current_app.db.clients.find_one({"email": form.email.data})
        if not cliente_data:
            flash("Usuário ou senha incorretos!", "danger")
            return redirect(url_for("pages.login"))
        cliente = Client(**cliente_data)

        if cliente and pbkdf2_sha256.verify(form.password.data, cliente.password):
            session["cliente_id"] = cliente._id
            session["email"] = cliente.email

        return redirect(url_for("pages.home"))

    return render_template("login.html", title="JA - Estética | Login", form=form)


@pages.route("/appointment/", methods=["GET", "POST"])
def appointment():

    if not session.get("email"):
        flash("Você precisa estar logado para agendar um procedimento.", "warning")
        return redirect(url_for("pages.login"))

    form = AppointmentForm()

    if form.validate_on_submit():

        if form.procedure_date.data < date.today():
            flash(
                "A data do procedimento não pode ser no passado. Por favor, escolha uma data futura.",
                "danger",
            )
            # Retorna o template sem validar, mostrando o alerta e mantendo o usuário na mesma página
            return render_template("appointment.html", form=form)

        elif form.procedure_time.data < time(8, 0) or form.procedure_time.data > time(
            17, 0
        ):
            flash("Nosso horário é das 08:00 às 17:00", "danger")
            # Retorna o template sem validar, mostrando o alerta e mantendo o usuário na mesma página
            return render_template("appointment.html", form=form)
        else:
            procedure = Appointment(
                _id=uuid4().hex,
                client_email=session.get("email"),
                procedure_name=form.procedure_name.data,
                _date=form.procedure_date.data.isoformat(),
                _time=form.procedure_time.data.isoformat(),
            )

            current_app.db.appointments.insert_one(asdict(procedure))

            flash("Procedimento agendado com sucesso!", "success")
            flash(
                f"{procedure.procedure_name} para o dia {procedure._date} às {procedure._time}",
                "success",
            )
            print(procedure)
            return redirect(url_for("pages.home"))

    return render_template(
        "appointment.html", title="JA - Estética | Agendamento", form=form
    )


@pages.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "success")
    return redirect(url_for(".login"))
