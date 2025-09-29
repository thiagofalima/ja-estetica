from app.app import create_app
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_talisman import Talisman

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
csp = {
    # Permite a maioria dos recursos (imagens, AJAX) do próprio site ('self')
    "default-src": ["'self'"],
    # Liberar o carregamento de CSS
    "style-src": [
        "'self'",
        "'unsafe-inline'",  # NECESSÁRIO se você tiver CSS inline (cuidado: pode ser um risco de segurança)
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css",  # Bootstrap CSS
        "https://fonts.googleapis.com",  # Google Fonts CSS
    ],
    "img-src": [
        "'self'",
        "data:",
    ],
    # Liberar o carregamento de JavaScript
    "script-src": [
        "'self'",
        "'unsafe-inline'",
        "https://cdnjs.cloudflare.com",  # Se usar outros libs/Bootstrap JS do CDN
        'https://cdn.jsdelivr.net', # Bootstrap JS,
        "https://*.googleapis.com",  # <--- GOOGLE MAPS SCRIPT AQUI
        "https://*.google.com",
    ],
    # Liberar o carregamento dos arquivos de fonte (Woff, TTF, etc.)
    "font-src": [
        "'self'",
        "https://fonts.gstatic.com",  # Arquivos de fontes do Google Fonts
    ],
    # Para liberar o conteúdo do google maps
    "frame-src": ["'self'", "https://*.google.com"],
}

# Inicialize o Talisman com a política de CSP customizada
Talisman(
    app,
    content_security_policy=csp,
    # Mantenha o Strict-Transport-Security (HSTS) para HTTPS
    strict_transport_security=True,
)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
