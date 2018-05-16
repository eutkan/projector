from flask import Flask, request, jsonify, render_template, redirect, url_for, abort
import db
import bcrypt
from datetime import datetime, timedelta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/projects')
def show_projects():
    projects = db.project.get_all()
    return render_template('projects/all.html', projects=projects)


@app.route('/project/add', methods=['POST'])
def add_project():
    name = request.form['name']
    db.project.add(name)
    return redirect(url_for('show_projects'))


@app.route('/project/<int:id>/delete', methods=['POST'])
def delete_project(id):
    db.project.delete(id)
    return redirect(url_for('show_projects'))


@app.route('/project/<int:id>')
def show_project(id):
    project = db.project.get(id)
    tasks = db.task.get_all_for_project(id)
    if not project:
        abort(404)

    return render_template('projects/show.html', project=project, tasks=tasks)


@app.route('/project/<int:id>/task/add', methods=['POST'])
def add_task_to_project(id):
    name = request.form['name']
    start_date = request.form['start_date']
    est_duration = request.form['est_duration']

    # Default start day to today
    if start_date.strip() == '':
        start = datetime.now()
    else:
        start = datetime.strptime(start_date, '%Y-%m-%d')

    # Add estimated duration to start date to find the end date
    end = start + timedelta(int(est_duration))

    db.task.add(id, name, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))
    return redirect(url_for('show_project', id=id))


@app.route('/task/<id>')
def show_task(id):
    task = db.task.get(id)
    if not task:
        abort(404)

    # check if the task is finished
    task['is_finished'] = task['end_date'] < datetime.now()

    free_employees = db.employee.get_all_available()
    return render_template('task/show.html', task=task, free_employees=free_employees)


@app.route('/task/<int:id>/delete', methods=['POST'])
def delete_task_from_project(id):
    project_id = request.form['project_id']
    db.task.delete(id)
    return redirect(url_for('show_project', id=project_id))


@app.route('/task/<int:id>/assign', methods=['POST'])
def assign_task_to_employee(id):
    employee_ids = request.form.getlist('employee_ids')
    db.task.assign_to_employees(id, employee_ids)

    return redirect(url_for('show_task', id=id))


@app.route('/employees')
def show_employees():
    employees = db.employee.get_all()
    return render_template('employee/all.html', employees=employees)


@app.route('/employee/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    db.employee.add(name)

    return redirect(url_for('show_employees'))


@app.route('/employee/<int:id>/delete', methods=['POST'])
def delete_employee(id):
    db.employee.delete(id)
    return redirect(url_for('show_employees'))


@app.route('/managers')
def show_managers():
    managers = db.manager.get_all()
    return render_template('manager/all.html', managers=managers)


@app.route('/manager/add', methods=['POST'])
def add_manager():
    name = request.form['name'].strip()
    password = request.form['password'].strip().encode()

    # hash the password before saving
    hash = bcrypt.hashpw(password, bcrypt.gensalt())
    db.manager.add(name, hash)

    return redirect(url_for('show_managers'))





if __name__ == '__main__':
    # TODO assign project to managers
    # TODO assign manager to projects
    # TODO delete manager
    # TODO triggers
    # TODO authorization

    app.run()
