import pymysql.cursors

connection = pymysql.connect(
    host='127.0.0.1',
    db='projector',
    user='root',
    password='',
    cursorclass=pymysql.cursors.DictCursor
)