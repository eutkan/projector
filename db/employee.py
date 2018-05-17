from db.connection import connection


def get_all():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM employee"
        cursor.execute(sql)
        return cursor.fetchall()


def get_all_available():
    with connection.cursor() as cursor:
        sql = "SELECT * FROM busyemployees WHERE busy_today = FALSE"
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


def get_assigned_for_task(task_id):
    with connection.cursor() as cursor:
        sql = """
            SELECT e.* FROM employeetask et 
                LEFT JOIN employee e ON et.employee_id = e.id 
            WHERE et.task_id = %(task_id)s
        """
        cursor.execute(sql, {
            'task_id': task_id
        })
        return cursor.fetchall()
