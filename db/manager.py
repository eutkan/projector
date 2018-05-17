from db.connection import connection


def get_all():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM manager"
        cursor.execute(sql)
        return cursor.fetchall()


def add(name, password_hash):
    with connection.cursor() as cursor:
        sql = "INSERT INTO manager (name, password_hash) VALUES (%s, %s)"
        cursor.execute(sql, (name, password_hash))
        connection.commit()


def delete(id):
    with connection.cursor() as cursor:
        sql = "DELETE FROM manager WHERE id = %(id)s"
        cursor.execute(sql, {
            'id': id
        })
        connection.commit()


def get(id):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM manager WHERE id = %(id)s"
        cursor.execute(sql, {
            'id': id
        })
        return cursor.fetchone()


def get_assigned_projects(id):
    with connection.cursor() as cursor:
        sql = """
            SELECT p.*
            FROM managerproject mp LEFT JOIN projectview p ON p.id = mp.project_id
            WHERE mp.manager_id = %(manager_id)s
        """
        cursor.execute(sql, {
            'manager_id': id
        })
        return cursor.fetchall()


def get_all_assigned_for_project(project_id):
    with connection.cursor() as cursor:
        sql = """
            SELECT m.*
            FROM managerproject mp LEFT JOIN manager m ON m.id = mp.manager_id
            WHERE mp.project_id = %(project_id)s
        """
        cursor.execute(sql, {
            'project_id': project_id
        })
        return cursor.fetchall()


def get_by_name(name):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM manager WHERE name = %(name)s"
        cursor.execute(sql, {
            'name': name
        })
        return cursor.fetchone()
