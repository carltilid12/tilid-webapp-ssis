from app import mysql

class student_model:
    @classmethod
    def create_student(cls, student_data):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to insert a new student
            insert_query = "INSERT INTO student (id, firstname, lastname, coursecode, studentyear, gender) VALUES (%s, %s, %s, %s, %s, %s)"
            
            # Execute the query with the student data
            cursor.execute(insert_query, (student_data['id'], student_data['firstname'], student_data['lastname'], student_data['coursecode'], student_data['studentyear'], student_data['gender']))
            
            # Commit the transaction to save the changes to the database
            connection.commit()

        except Exception as e:
            # Handle any errors, such as duplicate student IDs
            connection.rollback()
            raise e
        finally:
            cursor.close()

    @classmethod
    def get_students(cls):
        connection = mysql.connection
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM student')
        data = cursor.fetchall()
        cursor.close()
        return data