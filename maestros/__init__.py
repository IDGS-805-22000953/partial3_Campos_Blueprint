from flask import Blueprint

maestros_bp = Blueprint('maestros', __name__)

from . import routes
