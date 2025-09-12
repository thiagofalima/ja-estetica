from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, PasswordField, SubmitField
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import InputRequired, Email, Length, EqualTo

# Criando formulário de cadastro


class RegisterForm(FlaskForm):
    name = StringField(
        "Nome Completo *",
        validators=[InputRequired(message="O nome completo é obrigatório.")]
    )
    birth_date = DateField(
        "Data de Nascimento*",
        validators=[InputRequired(message="A data de nascimento é obrigatória.")],
    )

    phone_number = StringField(
        "Celular com DDD *",
        validators=[InputRequired(message="O celular é obrigatório."),
                    Length(min=11, message="O celular precisa ter 11 digitos.")]
    )

    email = EmailField(
        "Email *",
        validators=[
            InputRequired(message="O email é obrigatório."),
            Email(message="Email inválido."),
        ],
    )
    password = PasswordField(
        "Senha *",
        validators=[
            InputRequired(message="A senha é obrigatória."),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres."),
        ],
    )

    confirm_password = PasswordField(
        "Confimar a Senha*",
        validators=[InputRequired(message="É necessário confirmar a senha"), 
                    EqualTo("password", message="As senhas devem ser iguais.")]
    )

    submit = SubmitField("Cadastrar")


# Criando formulário de Login
class LoginForm(FlaskForm):

    email = EmailField(
        "Email *", validators=[InputRequired(message="O email é obrigatório.")]
    )

    password = PasswordField(
        "Senha *", validators=[InputRequired(message="A senha é obrigatória.")]
    )

    recaptcha = RecaptchaField()

    submit = SubmitField("Entrar")


