from app import mysql

class college_model:
    @classmethod
    def get_colleges(cls):
        connection = mysql.connection
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM college')
        data = cursor.fetchall()
        cursor.close()
        return data