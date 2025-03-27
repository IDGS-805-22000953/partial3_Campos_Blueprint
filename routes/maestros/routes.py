from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models.models import db, Alumnos, Maestros, Preguntas, Examenes, Respuestas
import forms
import logging

maestros_bp = Blueprint('maestros', __name__)
@maestros_bp.route('/examen', methods=['GET', 'POST'])
@login_required
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

@maestros_bp.route('/registrar_maestros', methods=['GET', 'POST'])
@login_required
def registrar_maestros():
    form = forms.MaestroForm(request.form)
    
    # Obtener todos los maestros registrados
    maestros = Maestros.query.all()
    
    if request.method == 'POST':
        nuevo_maestro = Maestros(
            nombre=form.nombre.data,
            apaterno=form.apaterno.data,
            amaterno=form.amaterno.data,
            email=form.email.data,
            telefono=form.telefono.data
        )
        db.session.add(nuevo_maestro)
        db.session.commit()
        flash('Maestro registrado exitosamente.', 'success')
        return redirect(url_for('maestros.registrar_maestros'))
    
    # Pasar los maestros a la plantilla
    return render_template('registrarMaestros.html', form=form, maestros=maestros)


@maestros_bp.route('/eliminar_maestro/<int:id>', methods=['POST'])
@login_required
def eliminar_maestro(id):
    maestro = Maestros.query.get(id)  
    if not maestro:
        flash('Maestro no encontrado', 'danger')
        return redirect(url_for('maestros.registrar_maestros'))

    db.session.delete(maestro)  
    db.session.commit()  
    flash('Maestro eliminado exitosamente.', 'success')
    return redirect(url_for('maestros.registrar_maestros'))


# Tu ruta para editar o registrar
@maestros_bp.route('/editar_maestro/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_maestro(id):
    maestro = Maestros.query.get(id)
    if not maestro:
        flash('Maestro no encontrado', 'danger')
        return redirect(url_for('maestros.registrar_maestros'))

    form = forms.MaestroForm(request.form, obj=maestro)  # Asignar datos al formulario

    if request.method == 'POST':  # Cuando el formulario es enviado
        if form.validate():  # Validación manual
            maestro.nombre = form.nombre.data
            maestro.apaterno = form.apaterno.data
            maestro.amaterno = form.amaterno.data
            maestro.email = form.email.data
            maestro.telefono = form.telefono.data

            db.session.commit()
            flash('Datos del maestro actualizados exitosamente.', 'success')
            return redirect(url_for('maestros.registrar_maestros'))
        else:
            flash('Por favor, completa todos los campos correctamente.', 'danger')

    return render_template('editarMaestro.html', form=form, maestro=maestro)
