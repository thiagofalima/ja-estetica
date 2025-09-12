from flask import Flask
from app.routes import pages
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()


def create_app():

    app = Flask(__name__)
    app.register_blueprint(pages)

    # Configurando Secret Key da aplicação
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    # Configurando Recaptcha Keys
    app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
    app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")

    return app
