import pymysql.cursors

connection = pymysql.connect(
    host='127.0.0.1',
    db='projector',
    user='projector',
    password='',
    cursorclass=pymysql.cursors.DictCursor
)