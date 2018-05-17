from db.connection import connection


def get_all():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM project"
        cursor.execute(sql)
        return cursor.fetchall()


def add(name, start_date='', est_duration=''):
    with connection.cursor() as cursor:
        sql = "INSERT INTO project(name) VALUES (%s)"
        cursor.execute(sql, (name,))
        connection.commit()


def get(id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM project WHERE id = %s"
        cursor.execute(sql, (id,))
        return cursor.fetchone()


def delete(id):
    with connection.cursor() as cursor:
        sql = "DELETE FROM project WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()


def assign_to_managers(project_id, manager_ids):
    with connection.cursor() as cursor:
        for manager_id in manager_ids:
            sql = "REPLACE INTO managerproject (project_id, manager_id) VALUES (%(project_id)s, %(manager_id)s)"
            cursor.execute(sql, {
                'project_id': project_id,
                'manager_id': manager_id
            })
        connection.commit()


def get_completed_for(manager_id):
    with connection.cursor() as cursor:
        cursor.callproc('completed_projects', (manager_id,))
        return cursor.fetchall()


def get_incomplete_for(manager_id):
    with connection.cursor() as cursor:
        cursor.callproc('incomplete_projects', (manager_id,))
        return cursor.fetchall()
