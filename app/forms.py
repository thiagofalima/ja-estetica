from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    name = StringField(
        'Nome Completo *',
        validators=[DataRequired(message="O nome completo é obrigatório.")]
    )
    birth_date = DateField(
        'Data de Nascimento',
        validators=[DataRequired(message="A data de nascimento é obrigatória.")]
    )
    email = EmailField(
        'Email *',
        validators=[DataRequired(message="O email é obrigatório."), Email(message="Email inválido.")]
    )
    password = PasswordField(
        'Senha *',
        validators=[
            DataRequired(message="A senha é obrigatória."),
            Length(min=8, message="A senha deve ter no mínimo 8 caracteres.")
        ]
    )
    submit = SubmitField('Entrar')