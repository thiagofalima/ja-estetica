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
from datetime import datetime, date, time, timedelta
from app.forms import RegisterForm, LoginForm, AppointmentForm
import time as tm
from app.models import Client, Appointment
import os.path
import os
from dotenv import load_dotenv

load_dotenv()

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
        else:
            flash("Usuário ou senha incorretos!", "danger")
            return redirect(url_for("pages.login"))

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
                appointment_date=datetime.now().isoformat()
            )

            current_app.db.appointments.insert_one(asdict(procedure))

            calendar_service = current_app.calendar_service 
        
            if calendar_service:
            # 2. Combinar data e hora do formulário em objetos datetime
                start_datetime_obj = datetime.combine(form.procedure_date.data, form.procedure_time.data)
                
                # 3. Calcular a hora de término (ex: 1 hora de duração)
                duration = timedelta(hours=1)
                end_datetime_obj = start_datetime_obj + duration

                # 4. Definir o fuso horário (AJUSTE CONFORME SUA LOCALIZAÇÃO)
                TIMEZONE = 'America/Sao_Paulo'
                
                # 5. Criar o corpo do evento
                event = {
                    'summary': f"{procedure.procedure_name} - Cliente: {session.get('email')}",
                    'location': 'Endereço da Clínica (Opcional)',
                    'description': f'Novo agendamento criado via App JA Estética.\nCliente: {session.get("email")}',
                    
                    # Formato RFC 3339 exigido pela API
                    'start': {
                        'dateTime': start_datetime_obj.isoformat(),
                        'timeZone': TIMEZONE,
                    },
                    'end': {
                        'dateTime': end_datetime_obj.isoformat(),
                        'timeZone': TIMEZONE,
                    },
                    
                    'reminders': {
                        'useDefault': True,
                    },
                }

                # 6. Inserir o evento no Google Calendar
                try:
                    # O calendarId='primary' se refere ao calendário principal da conta de serviço/autorizada
                    event_result = calendar_service.events().insert(
                        calendarId=os.getenv("CALENDAR_ID"), 
                        body=event
                    ).execute()
                    
                    flash("Evento criado no Google Agenda com sucesso!", "success")
                    # print(f"Evento criado: {event_result.get('htmlLink')}")
                    
                except Exception as e:
                    # Trata a exceção, caso haja falha de autenticação ou API
                    flash(f"Erro ao criar evento no Google Agenda. Verifique as credenciais: {e}", "danger")
        

            flash(f"""Procedimento agendado com sucesso!
            {procedure.procedure_name} para o dia {procedure._date} às {procedure._time}.
            """,
                "success",
            )
            print(procedure)
            return redirect(url_for("pages.appointment"))

    return render_template(
        "appointment.html", title="JA - Estética | Agendamento", form=form
    )


@pages.route("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "success")
    return redirect(url_for(".login"))
