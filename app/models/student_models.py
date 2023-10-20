from app import mysql

class student_model:
    @classmethod
    def get_students(cls):
        connection = mysql.connection
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student')
        data = cursor.fetchall()
        cursor.close()
        return data