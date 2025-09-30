from flask import Flask
from app.routes import pages
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Carrega as variáveis de ambiente
load_dotenv()

SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_SERVICE_KEY_PATH')

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Carrega as credenciais da conta de serviço e constrói o objeto de serviço da API."""
    try:
        credentials = Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        # Constrói o objeto de serviço da API
        service = build('calendar', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print(f"Erro ao carregar o Serviço de Calendário: {e}")
        return None

# App factory
def create_app():

    app = Flask(__name__)
    app.register_blueprint(pages)

    # Configurando Secret Key da aplicação
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Configurando DB
    app.config["DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.db = MongoClient(app.config["DATABASE_URI"]).ja_estetica

    # Config do serviço de Calendário
    app.calendar_service = get_calendar_service()

    # Configurando Recaptcha Keys
    # app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("RECAPTCHA_PUBLIC_KEY")
    # app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("RECAPTCHA_PRIVATE_KEY")

    return app
