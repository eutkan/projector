from flask import Flask, request, render_template, redirect, url_for, abort, session, flash
import db
import auth
from auth import admins
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/projects')
def show_projects():
    projects = db.project.get_all()
    return render_template('projects/all.html', projects=projects)


@app.route('/projects/completed')
@app.route('/projects/completed/<int:manager_id>')
def show_completed_projects(manager_id='ALL'):
    completed_projects = db.project.get_completed_for(manager_id)
    if manager_id == 'ALL':
        title = 'Showing all completed projects'
    else:
        title = 'Showing completed projects for the manager #{}'.format(manager_id)

    return render_template('projects/all-filtered.html', projects=completed_projects, title=title)


@app.route('/projects/incomplete')
@app.route('/projects/incomplete/<int:manager_id>')
def show_incomplete_projects(manager_id='ALL'):
    incomplete_projects = db.project.get_incomplete_for(manager_id)
    if manager_id == 'ALL':
        title = 'Showing all incomplete projects'
    else:
        title = 'Showing incomplete projects for the manager #{}'.format(manager_id)

    return render_template('projects/all-filtered.html', projects=incomplete_projects, title=title)


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
    managers = db.manager.get_all()
    assignees = db.manager.get_all_assigned_for_project(id)

    if not project:
        abort(404)

    return render_template('projects/show.html', project=project, tasks=tasks, managers=managers, assignees=assignees)


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


@app.route('/project/<int:id>/assign', methods=['POST'])
def assign_project_to_manager(id):
    manager_ids = request.form.getlist('manager_ids')

    db.project.assign_to_managers(id, manager_ids)
    return redirect(url_for('show_project', id=id))


@app.route('/task/<int:id>')
def show_task(id):
    task = db.task.get(id)
    if not task:
        abort(404)

    # check if the task is finished
    task['is_finished'] = task['end_date'] < datetime.now()

    assigned_employees = db.employee.get_assigned_for_task(id)
    free_employees = db.employee.get_all_available()
    return render_template('task/show.html', task=task, free_employees=free_employees,
                           assigned_employees=assigned_employees)


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
    hash = auth.password.hash(password)
    db.manager.add(name, hash)

    return redirect(url_for('show_managers'))


@app.route('/manager/<int:id>/delete', methods=['POST'])
def delete_manager(id):
    db.manager.delete(id)
    return redirect(url_for('show_managers'))


@app.route('/manager/<int:id>')
def show_manager(id):
    manager = db.manager.get(id)
    assigned_projects = db.manager.get_assigned_projects(id)
    if not manager:
        abort(404)

    return render_template('manager/show.html', manager=manager, assigned_projects=assigned_projects)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')

    name = request.form['name']
    password = request.form['password'].encode()

    admin = get_admin(name)
    if admin and admin['password'].encode() == password:
        # set logged in user as admin
        session['user_id'] = -1
        flash('Welcome, {}'.format(admin['name']), 'success')
        return redirect(url_for('home'))

    manager = db.manager.get_by_name(name)
    if not manager:
        return redirect(url_for('login'))

    # check password
    if not auth.password.check_hash(password, manager['password_hash'].encode()):
        return redirect(url_for('login'))

    # start session
    session['user_id'] = manager['id']
    flash('Welcome, {}'.format(manager['name']), 'success')
    return redirect(url_for('show_manager', id=manager['id']))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))


@app.template_global()
def is_logged_in():
    return 'user_id' in session


@app.template_global()
def get_user():
    if 'user_id' in session:
        user = db.manager.get(session['user_id'])
        return user
    return None


@app.template_global()
def is_admin():
    return 'user_id' in session and session['user_id'] <= 0


def get_admin(name):
    for admin in admins:
        if admin['name'] == name:
            return admin
    return None


@app.before_request
def check_is_logged_in():
    if request.path == url_for('login'):
        return
    if not is_logged_in():
        flash('You need to log in first', 'error')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
