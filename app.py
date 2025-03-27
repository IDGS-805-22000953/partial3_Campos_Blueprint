import logging
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import DevelopmentConfig
from auth.routes import auth_bp
from routes.alumnos.routes import alumnos_bp
from routes.maestros.routes import maestros_bp
import forms
import datetime
from models.models import db, Alumnos, Preguntas, Examenes, Respuestas
import warnings
from sqlalchemy.exc import SAWarning


# Configuracion del logging
logging.basicConfig(
    filename='app.log', level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__, template_folder="templates")
csrf = CSRFProtect()
warnings.filterwarnings("ignore", category=SAWarning)


# Configuración de la aplicación
app.config.from_object(DevelopmentConfig)

# Inicialización de la base de datos
db.init_app(app)

# Configuración del Login Manager
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login' 

# Cargar usuario para flask-login
@login_manager.user_loader
def load_user(user_id):
    from models.models import User
    return User.query.get(int(user_id))

# Registrar los Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(alumnos_bp, url_prefix='/alumnos')
app.register_blueprint(maestros_bp, url_prefix='/maestros')


with app.app_context():
    print("Intentando crear tablas...")
    db.create_all()
    print("Tablas creadas.")
    
""" @app.errorhandler(404)
def page_not_found(e):
    logging.warning("Página no encontrada: 404")
    return render_template('404.html'), 404 """

@app.route('/')
def home():
    return redirect(url_for('auth.login'))  




if __name__ == '__main__':
    logging.info("Inicio de la aplicación Flask")
    csrf.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)