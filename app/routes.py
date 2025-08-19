from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from sqlalchemy.exc import SQLAlchemyError
from . import db
from .models import Host, Task, Change
from .forms import HostForm, TaskForm, ChangeForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    hosts = Host.query.order_by(Host.id.asc()).all()
    return render_template('index.html', hosts=hosts)

# Hosts CRUD

@main.route('/hosts')
def hosts():
    hosts = Host.query.order_by(Host.id.asc()).all()
    return render_template('hosts.html', hosts=hosts)

@main.route('/hosts/add', methods=['GET', 'POST'])
def add_host():
    form = HostForm()
    if form.validate_on_submit():
        try:
            host = Host(
                hostname=form.hostname.data.strip(),
                ip_address=form.ip_address.data.strip(),
                os=form.os.data.strip() if form.os.data else None,
                tags=form.tags.data.strip() if form.tags.data else None
            )
            db.session.add(host)
            db.session.commit()
            flash('Host added successfully.')
            return redirect(url_for('main.hosts'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error adding host. Please try again.')
            return render_template('add_host.html', form=form)
    return render_template('add_host.html', form=form)

@main.route('/hosts/edit/<int:id>', methods=['GET', 'POST'])
def edit_host(id: int):
    host = Host.query.get_or_404(id)
    form = HostForm(obj=host)
    if form.validate_on_submit():
        try:
            host.hostname = form.hostname.data.strip()
            host.ip_address = form.ip_address.data.strip()
            host.os = form.os.data.strip() if form.os.data else None
            host.tags = form.tags.data.strip() if form.tags.data else None
            db.session.commit()
            flash('Host updated successfully.')
            return redirect(url_for('main.hosts'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error updating host. Please try again.')
            return render_template('edit_host.html', form=form, host=host)
    return render_template('edit_host.html', form=form, host=host)

@main.route('/hosts/delete/<int:id>', methods=['POST'])
def delete_host(id: int):
    # CSRF is handled globally; double check the form includes a CSRF token
    host = Host.query.get_or_404(id)
    try:
        db.session.delete(host)
        db.session.commit()
        flash('Host and related records deleted.')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error deleting host. Please try again.')
    return redirect(url_for('main.hosts'))


# Tasks CRUD


@main.route('/tasks')
def tasks():
    tasks = Task.query.order_by(Task.id.asc()).all()
    return render_template('tasks.html', tasks=tasks)

@main.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    form.host_id.choices = [(h.id, h.hostname) for h in Host.query.order_by(Host.hostname).all()]
    if form.validate_on_submit():
        try:
            task = Task(host_id=form.host_id.data, description=form.description.data.strip())
            db.session.add(task)
            db.session.commit()
            flash('Task added successfully.')
            return redirect(url_for('main.tasks'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error adding task. Please try again.')
            return render_template('add_task.html', form=form)
    return render_template('add_task.html', form=form)

@main.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id: int):
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    form.host_id.choices = [(h.id, h.hostname) for h in Host.query.order_by(Host.hostname.asc()).all()]
    if form.validate_on_submit():
        try:
            task.host_id = form.host_id.data
            task.description = form.description.data.strip()
            db.session.commit()
            flash('Task updated successfully.')
            return redirect(url_for('main.tasks'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error updating task. Please try again.')
            return render_template('edit_task.html', form=form, task=task)
    return render_template('edit_task.html', form=form, task=task)

    
@main.route('/tasks/delete/<int:id>', methods=['POST'])
def delete_task(id: int):
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted.')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error deleting task. Please try again.')
    return redirect(url_for('main.tasks'))

# Changes CRUD

@main.route('/changes')
def changes():
    changes = Change.query.order_by(Change.id.asc()).all()
    return render_template('changes.html', changes=changes)

@main.route('/changes/add', methods=['GET', 'POST'])
def add_change():
    form = ChangeForm()
    form.host_id.choices = [(h.id, h.hostname) for h in Host.query.order_by(Host.hostname.asc()).all()]
    if form.validate_on_submit():
        try:
            change = Change(host_id=form.host_id.data, summary=form.summary.data.strip())
            db.session.add(change)
            db.session.commit()
            flash('Change logged successfully.')
            return redirect(url_for('main.changes'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error logging change. Please try again.')
            return render_template('add_change.html', form=form)
    return render_template('add_change.html', form=form)

@main.route('/changes/edit/<int:id>', methods=['GET', 'POST'])
def edit_change(id: int):
    change = Change.query.get_or_404(id)
    form = ChangeForm(obj=change)
    form.host_id.choices = [(h.id, h.hostname) for h in Host.query.order_by(Host.hostname.asc()).all()]
    if form.validate_on_submit():
        try:
            change.host_id = form.host_id.data
            change.summary = form.summary.data.strip()
            db.session.commit()
            flash("Change updated successfully.")
            return redirect(url_for('main.changes'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error updating change. Please try again.')
            return render_template('edit_change.html', form=form, change=change)
    return render_template('edit_change.html', form=form, change=change)

@main.route('/changes/delete/<int:id>', methods=['POST'])
def delete_change(id: int):
    change = Change.query.get_or_404(id)
    try:
        db.session.delete(change)
        db.session.commit()
        flash('Change deleted.')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error deleting change. Please try again.')
    return redirect(url_for('main.changes'))
