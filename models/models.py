from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db=SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    grupo = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    
class Maestros(db.Model):
    __tablename__ = 'maestros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apaterno = db.Column(db.String(50), nullable=False)
    amaterno = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.datetime.now)

class Preguntas(db.Model):
    __tablename__ = 'preguntas'
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(255), nullable=False)
    opcion_a = db.Column(db.String(100), nullable=False)
    opcion_b = db.Column(db.String(100), nullable=False)
    opcion_c = db.Column(db.String(100), nullable=False)
    opcion_d = db.Column(db.String(100), nullable=False)
    respuesta_correcta = db.Column(db.String(1), nullable=False)  
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

class Examenes(db.Model):
    __tablename__ = 'examenes'
    id = db.Column(db.Integer, primary_key=True)
    alumno_id = db.Column(db.Integer, db.ForeignKey('alumnos.id'), nullable=False)
    fecha_realizacion = db.Column(db.DateTime, default=datetime.datetime.now)
    calificacion = db.Column(db.Float, nullable=True)
    alumno = db.relationship('Alumnos', backref=db.backref('examenes', lazy=True))

class Respuestas(db.Model):
    __tablename__ = 'respuestas'
    id = db.Column(db.Integer, primary_key=True)
    examen_id = db.Column(db.Integer, db.ForeignKey('examenes.id'), nullable=False)
    pregunta_id = db.Column(db.Integer, db.ForeignKey('preguntas.id'), nullable=False)
    respuesta_elegida = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C' o 'D'
    examen = db.relationship('Examenes', backref=db.backref('respuestas', lazy=True))
    pregunta = db.relationship('Preguntas', backref=db.backref('respuestas', lazy=True))