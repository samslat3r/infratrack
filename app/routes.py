from flask import render_template, redirect, url_for, flash, request
from flask import Blueprint
from . import db
from .models import Host, Task, Change
from .forms import HostForm, TaskForm, ChangeForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    hosts = Host.query.all()
    return render_template('index.html', hosts=hosts)


# Hosts CRUD


@main.route('/hosts')
def hosts():
    hosts = Host.query.all()
    return render_template('hosts.html', hosts=hosts)

@main.route('/hosts/add', methods=['GET', 'POST'])
def add_host():
    form = HostForm()
    if request.method == 'POST' and form.validate_on_submit():
        host = Host(
            hostname=form.hostname.data,
            ip_address=form.ip_address.data,
            os=form.os.data,
            tags=form.tags.data
        )
        db.session.add(host)
        db.session.commit()
        flash('Host added successfully.')
        return redirect(url_for('main.hosts'))
    return render_template('add_host.html', form=form)

@main.route('/hosts/edit/<int:id>', methods=['GET', 'POST'])
def edit_host(id):
    host = Host.query.get_or_404(id)
    form = HostForm(obj=host)
    if request.method == 'POST' and form.validate_on_submit():
        host.hostname = form.hostname.data
        host.ip_address = form.ip_address.data
        host.os = form.os.data
        host.tags = form.tags.data
        db.session.commit()
        flash('Host updated successfully.')
        return redirect(url_for('main.hosts'))
    return render_template('edit_host.html', form=form, host=host)

@main.route('/hosts/delete/<int:id>', methods=['POST'])
def delete_host(id):
    host = Host.query.get_or_404(id)
    db.session.delete(host)
    db.session.commit()
    flash('Host deleted.')
    return redirect(url_for('main.hosts'))


# Tasks CRUD


@main.route('/tasks')
def tasks():
    tasks = Task.query.all()
    return render_template('tasks.html', tasks=tasks)

@main.route('/tasks/add', methods=['GET', 'POST'])
def add_task():
    form = TaskForm()
    form.host_id.choices = [(h.id, h.hostname) for h in Host.query.order_by(Host.hostname).all()]

    if request.method == 'POST' and form.validate_on_submit():
        task = Task(
            host_id=form.host_id.data,
            description=form.description.data
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully.')
        return redirect(url_for('main.tasks'))
    return render_template('add_task.html', form=form)

@main.route('/tasks/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    form.host_id.choices = [(h.id, h.hostname) for h in Host.query.order_by(Host.hostname).all()]

    if request.method == 'POST' and form.validate_on_submit():
        task.host_id = form.host_id.data
        task.description = form.description.data
        db.session.commit()
        flash('Task updated successfully.')
        return redirect(url_for('main.tasks'))
    return render_template('edit_task.html', form=form, task=task)


@main.route('/tasks/delete/<int:id>', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted.')
    return redirect(url_for('main.tasks'))

# Changes CRUD

@main.route('/changes')
def changes():
    changes = Change.query.all()
    return render_template('changes.html', changes=changes)

@main.route('/changes/add', methods=['GET', 'POST'])
def add_change():
    form = ChangeForm()
    form.host_id.choices = [(h.id, h.hostname) for h in Host.query.order_by(Host.hostname).all()]

    if request.method == 'POST' and form.validate_on_submit():
        change = Change(
            host_id=form.host_id.data,
            summary=form.summary.data
        )
        db.session.add(change)
        db.session.commit()
        flash('Change logged successfully.')
        return redirect(url_for('main.changes'))
    return render_template('add_change.html', form=form)

@main.route('/changes/edit/<int:id>', methods=['GET', 'POST'])
def edit_change(id):
    change = Change.query.get_or_404(id)
    form = ChangeForm(obj=change)
    form.host_id.choices = [(h.id, h.hostname) for h in Host.query.order_by(Host.hostname).all()]

    if request.method == 'POST' and form.validate_on_submit():
        change.host_id = form.host_id.data
        change.summary = form.summary.data
        db.session.commit()
        flash('Change updated successfully.')
        return redirect(url_for('main.changes'))
    return render_template('edit_change.html', form=form, change=change)

@main.route('/changes/delete/<int:id>', methods=['POST'])
def delete_change(id):
    change = Change.query.get_or_404(id)
    db.session.delete(change)
    db.session.commit()
    flash('Change deleted.')
    return redirect(url_for('main.changes'))