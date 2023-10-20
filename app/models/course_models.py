from app import mysql

class course_model:
    @classmethod
    def get_courses(cls):
        connection = mysql.connection
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM course')
        data = cursor.fetchall()
        cursor.close()
        return data