from wtforms import Form
 
from wtforms import StringField, SelectField, IntegerField, SubmitField, DateField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired, Length

 
class AlumnoForm(Form):
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=2, max=50, message='Ingrese un nombre válido')
    ])
    apaterno = StringField('Apellido Paterno', [
        validators.DataRequired(message='El campo es requerido')
    ])
    amaterno = StringField('Apellido Materno', [
        validators.DataRequired(message='El campo es requerido')
    ])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', 
        validators=[validators.DataRequired(message='Ingrese una fecha válida')])
    grupo = StringField('Grupo', [
        validators.DataRequired(message='El campo es requerido')
    ])

class AlumnoFormEditar(Form):
    id = IntegerField('ID', [
        validators.NumberRange(min=1, message='ID no válido')
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=2, max=50, message='Ingrese un nombre válido')
    ])
    apaterno = StringField('Apellido Paterno', [
        validators.DataRequired(message='El campo es requerido')
    ])
    amaterno = StringField('Apellido Materno', [
        validators.DataRequired(message='El campo es requerido')
    ])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', 
        validators=[validators.DataRequired(message='Ingrese una fecha válida')])
    grupo = StringField('Grupo', [
        validators.DataRequired(message='El campo es requerido')
    ])
    

class PreguntaForm(Form):
    pregunta = StringField('Pregunta', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=10, max=255, message='Ingrese una pregunta válida')
    ])
    opcion_a = StringField('Opción A', [validators.DataRequired(message='Este campo es obligatorio')])
    opcion_b = StringField('Opción B', [validators.DataRequired(message='Este campo es obligatorio')])
    opcion_c = StringField('Opción C', [validators.DataRequired(message='Este campo es obligatorio')])
    opcion_d = StringField('Opción D', [validators.DataRequired(message='Este campo es obligatorio')])
    respuesta_correcta = SelectField('Respuesta Correcta', 
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')],
        validators=[validators.DataRequired(message='Seleccione una respuesta correcta')]
    )
    
class BuscarAlumnoForm(Form):
    nombre = StringField('Nombre', validators=[DataRequired(message='El campo es obligatorio')])
    apaterno = StringField('Apellido Paterno', validators=[DataRequired(message='El campo es obligatorio')])
    submit = SubmitField('Buscar Alumno')
    
class SeleccionarGrupoForm(Form):
    grupo = SelectField('Grupo', choices=[], validators=[DataRequired()])
    submit = SubmitField('Ver Calificaciones')

