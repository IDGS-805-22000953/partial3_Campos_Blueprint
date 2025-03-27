from flask import Blueprint

alumnos_bp = Blueprint('alumnos', __name__)

from . import routes
