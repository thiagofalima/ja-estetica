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

    return app
