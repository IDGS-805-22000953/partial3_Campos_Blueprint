from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models.models import db, Alumnos, Preguntas, Examenes, Respuestas
import forms
import logging

maestros_bp = Blueprint('maestros', __name__)
@maestros_bp.route('/examen', methods=['GET', 'POST'])
def examen():
    create_form = forms.PreguntaForm(request.form)
    preguntas = Preguntas.query.all()
    if request.method == 'POST':
        pregunta = Preguntas(
            pregunta=create_form.pregunta.data,
            opcion_a=create_form.opcion_a.data,
            opcion_b=create_form.opcion_b.data,
            opcion_c=create_form.opcion_c.data,
            opcion_d=create_form.opcion_d.data,
            respuesta_correcta=create_form.respuesta_correcta.data
        )
        db.session.add(pregunta)
        db.session.commit()
        logging.info(f"Pregunta agregada: {pregunta.pregunta}")
        flash('Pregunta agregada exitosamente', 'success')
        return redirect(url_for('maestros.examen'))
    return render_template('examen.html', form=create_form, preguntas=preguntas)
