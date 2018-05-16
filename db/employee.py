from db.connection import connection


def get_all():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM employee"
        cursor.execute(sql)
        return cursor.fetchall()


def get_all_available():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM busyemployees WHERE busy_today = false"
        cursor.execute(sql)
        return cursor.fetchall()


def add(name):
    with connection.cursor() as cursor:
        sql = "INSERT INTO employee(name) VALUES (%s)"
        cursor.execute(sql, (name,))
        connection.commit()


def delete(id):
    with connection.cursor() as cursor:
        sql = "DELETE FROM employee WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()
