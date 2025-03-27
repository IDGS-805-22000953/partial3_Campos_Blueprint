from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models.models import db, Alumnos, Preguntas, Examenes, Respuestas
import forms
import logging
import datetime

alumnos_bp = Blueprint('alumnos', __name__)


@alumnos_bp.route("/index")
@login_required
def index():
    logging.info("Acceso a la página de inicio")
    create_form = forms.AlumnoFormEditar(request.form)
    return render_template("index.html", form=create_form)

@alumnos_bp.route('/alumnos1', methods=['GET', 'POST'])
@login_required
def Alumnos1():
    create_form = forms.AlumnoFormEditar(request.form)
    if request.method == 'POST':
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apaterno=create_form.apaterno.data,
            amaterno=create_form.amaterno.data,
            fecha_nacimiento=create_form.fecha_nacimiento.data,
            grupo=create_form.grupo.data
        )
        db.session.add(alum)
        db.session.commit()
        logging.info(f"Alumno agregado: {alum.nombre} {alum.apaterno}, Grupo: {alum.grupo}")
    return render_template('index.html', form=create_form)

@alumnos_bp.route('/realizar_examen', methods=['GET', 'POST'])
@login_required
def realizar_examen():
    create_form = forms.BuscarAlumnoForm(request.form)
    alumno = None
    preguntas = Preguntas.query.all()
    if request.method == 'POST':
        nombre = request.form.get('nombre')  
        apaterno = request.form.get('apaterno')
        alumno = Alumnos.query.filter_by(nombre=nombre, apaterno=apaterno).first()
        if not alumno:
            logging.warning(f"Intento de búsqueda de alumno fallido: {nombre} {apaterno}")
            flash('Alumno no encontrado')
            return redirect(url_for('realizar_examen')) 
        hoy = datetime.date.today()
        edad = hoy.year - alumno.fecha_nacimiento.year - ((hoy.month, hoy.day) < (alumno.fecha_nacimiento.month, alumno.fecha_nacimiento.day))
        logging.info(f"Alumno encontrado: {alumno.nombre} {alumno.apaterno}, Edad: {edad}")
        return render_template('realizarExamen.html', form=create_form, alumno=alumno, preguntas=preguntas, edad=edad)
    return render_template('realizarExamen.html', form=create_form, alumno=alumno, preguntas=preguntas)

@alumnos_bp.route('/guardar_examen', methods=['POST'])
@login_required
def guardar_examen():
    alumno_id = request.form.get('alumno_id')
    alumno = Alumnos.query.get(alumno_id)
    if not alumno:
        logging.error("Intento de guardar examen sin alumno válido")
        flash('Error: Alumno no encontrado.', 'danger')
        return redirect(url_for('alumnos.realizar_examen'))

    examen = Examenes(alumno_id=alumno_id)
    db.session.add(examen)
    db.session.commit()

    respuestas_correctas = 0
    preguntas = Preguntas.query.all()
    for pregunta in preguntas:
        respuesta_elegida = request.form.get(f'pregunta_{pregunta.id}')
        if respuesta_elegida:
            respuesta = Respuestas(
                examen_id=examen.id,
                pregunta_id=pregunta.id,
                respuesta_elegida=respuesta_elegida
            )
            db.session.add(respuesta)
            if respuesta_elegida == pregunta.respuesta_correcta:
                respuestas_correctas += 1

    calificacion = (respuestas_correctas / len(preguntas)) * 10 if preguntas else 0
    examen.calificacion = calificacion
    db.session.commit()
    
    logging.info(f"Examen guardado: Alumno {alumno.nombre} {alumno.apaterno}, Calificación: {calificacion:.2f}")
    flash(f'Examen guardado con éxito. Calificación: {calificacion:.2f}', 'success')
    return redirect(url_for('alumnos.ver_calificaciones', grupo=alumno.grupo))

@alumnos_bp.route('/ver_calificaciones', methods=['GET', 'POST'])
@login_required
def ver_calificaciones():
    create_form = forms.SeleccionarGrupoForm(request.form)  
    grupos = db.session.query(Alumnos.grupo).distinct().all()
    grupos = [g[0] for g in grupos]
    create_form.grupo.choices = [(g, g) for g in grupos]
    alumnos = None
    if request.method == 'POST':
        grupo_seleccionado = create_form.grupo.data
        alumnos = (
            db.session.query(Alumnos, Examenes)
            .join(Examenes, Alumnos.id == Examenes.alumno_id)
            .filter(Alumnos.grupo == grupo_seleccionado)
            .all()
        )
        logging.info(f"Consulta de calificaciones para el grupo: {grupo_seleccionado}")
    return render_template('ver_calificaciones.html', form=create_form, alumnos=alumnos)
