from db.connection import connection


def get_all_for_project(project_id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM task WHERE project_id = %s"
        cursor.execute(sql, (project_id,))
        return cursor.fetchall()


def add(project_id, name, start_date, end_date):
    with connection.cursor() as cursor:
        sql = "INSERT INTO task(name, project_id, start_date, end_date) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name, project_id, start_date, end_date))
        connection.commit()


def delete(id):
    with connection.cursor() as cursor:
        sql = "DELETE FROM task WHERE id = %s"
        cursor.execute(sql, (id))
        connection.commit()


def get(id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM task WHERE id = %s"
        cursor.execute(sql, (id,))
        return cursor.fetchone()


def assign_to_employees(task_id, employee_ids):
    with connection.cursor() as cursor:
        for employee_id in employee_ids:
            sql = "REPLACE INTO employeetask (employee_id, task_id) VALUES (%s, %s)"
            cursor.execute(sql, (employee_id, task_id))
        connection.commit()
