from flask_wtf import FlaskForm
from wtforms import (StringField,
                      DateField,
                      TimeField, 
                      EmailField, 
                      PasswordField, 
                      SubmitField,
                      SelectField)
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

# Criando formulário de cadastro
class RegisterForm(FlaskForm):
    name = StringField(
        "Nome Completo *",
        validators=[DataRequired(message="O nome completo é obrigatório.")]
    )
    birth_date = DateField(
        "Data de Nascimento*",
        validators=[DataRequired(message="A data de nascimento é obrigatória.")],
    )

    phone_number = StringField(
        "Celular com DDD *",
        validators=[DataRequired(message="O celular é obrigatório."),
                    Length(min=11, message="O celular precisa ter 11 digitos.")]
    )

    email = EmailField(
        "Email *",
        validators=[
            DataRequired(message="O email é obrigatório."),
            Email(message="Email inválido."),
        ],
    )
    password = PasswordField(
        "Senha *",
        validators=[
            DataRequired(message="A senha é obrigatória."),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
    )

    confirm_password = PasswordField(
        "Confimar a Senha*",
        validators=[DataRequired(message="É necessário confirmar a senha"), 
                    EqualTo("password", message="As senhas devem ser iguais.")]
    )

    submit = SubmitField("Cadastrar")


# Criando formulário de Login
class LoginForm(FlaskForm):

    email = EmailField(
        "Email *", validators=[DataRequired(message="O email é obrigatório.")]
    )

    password = PasswordField(
        "Senha *", validators=[DataRequired(message="A senha é obrigatória.")]
    )

    recaptcha = RecaptchaField()

    submit = SubmitField("Entrar")

# Criando formulário para agendamento de procedimento 
class AppointmentForm(FlaskForm):
    
    procedure_name = SelectField(
        "Procedimento *",
        validators=[DataRequired(message="Escolha o procedimento.")],
        choices=[
            "*Escolha*",
            "Design de Sobrancelhas",
            "Brow Lamination",
            "Lash Lifting",
            "Detox Corporal",
            "Limpeza de Pele",
            "Depilação a Laser"
        ]
    )

    procedure_date = DateField(
        "Data", format='%Y-%m-%d',
        validators=[DataRequired(message="Escolha o dia do seu procedimento.")],
    )

    procedure_time = TimeField(
        "Hora", format="%H:%M",
        validators=[DataRequired(message="Escolha o horário do seu procedimento.")]
    )

    submit = SubmitField("Agendar")

    