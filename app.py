from flask import Flask, jsonify, request
from flask_cors import CORS
from routes.generate import generate_bp
from routes.upload import upload_bp
import os
import logging
from werkzeug.middleware.proxy_fix import ProxyFix

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Ayuda con proxies en producción
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

# Configurar CORS para entorno de producción
allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')
CORS(app, origins=allowed_origins.split(','), supports_credentials=True)

# Registrar blueprints
app.register_blueprint(generate_bp, url_prefix="/api")
app.register_blueprint(upload_bp, url_prefix="/api")

# Manejadores de errores
@app.errorhandler(404)
def not_found(error):
    logger.error(f"Recurso no encontrado: {request.path}")
    return jsonify({"error": "El recurso solicitado no existe"}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Error interno del servidor: {str(error)}")
    return jsonify({"error": "Error interno del servidor"}), 500

@app.errorhandler(400)
def bad_request(error):
    logger.error(f"Solicitud incorrecta: {str(error)}")
    return jsonify({"error": "Solicitud incorrecta o malformada"}), 400

# Ruta de verificación de salud para monitorización
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

# Middleware para logging de solicitudes
@app.before_request
def log_request_info():
    if not request.path.startswith('/health'):  # Evitar logging excesivo por health checks
        logger.info(f"Solicitud {request.method} a {request.path} desde {request.remote_addr}")

@app.after_request
def log_response_info(response):
    if not request.path.startswith('/health'):
        logger.info(f"Respuesta {response.status_code} para {request.method} a {request.path}")
    return response

# Solo para ejecución directa (desarrollo), en producción usará gunicorn
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)