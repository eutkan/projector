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