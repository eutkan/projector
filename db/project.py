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