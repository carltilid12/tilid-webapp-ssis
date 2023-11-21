from app import mysql

class student_model:
    @classmethod
    def delete_student(cls, student_id):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to delete a student by ID
            delete_query = "DELETE FROM student WHERE id = %s"
            
            # Execute the query with the student ID
            cursor.execute(delete_query, (student_id,))
            
            # Commit the transaction to save the changes to the database
            connection.commit()
            return True
        except Exception as e:
            # Handle any errors that may occur during the delete operation
            connection.rollback()
            raise e
        finally:
            cursor.close()

    @classmethod
    def update_student(cls, student_data):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to update an existing student
            update_query = "UPDATE student SET firstname = %s, lastname = %s, coursecode = %s, studentyear = %s, gender = %s WHERE id = %s"
            print(update_query)
            print(student_data)
            # Execute the query with the student data
            cursor.execute(update_query, (student_data['firstname'], student_data['lastname'], student_data['coursecode'], student_data['studentyear'], student_data['gender'], student_data['id']))
            
            # Commit the transaction to save the changes to the database
            connection.commit()

        except Exception as e:
            # Handle any errors that may occur during the update
            connection.rollback()
            raise e
        finally:
            cursor.close()
            
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
        cursor.execute('SELECT student.id, student.firstname, student.lastname, student.coursecode, \
                        student.studentyear, student.gender, \
                        CONCAT(college.collegename, " (", college.collegecode , ")") AS collegename\
                        FROM student\
                        JOIN course ON student.coursecode = course.coursecode\
                        JOIN college on course.collegecode = college.collegecode')
        data = cursor.fetchall()
        cursor.close()
        return data
    
    @classmethod
    def get_student_by_id(cls, student_id):
        connection = mysql.connection
        cursor = connection.cursor()

        try:
            query = "SELECT student.id, student.firstname, student.lastname, \
                        student.studentyear, student.gender,\
                        CONCAT(course.coursename, ' (', course.coursecode , ')') AS coursename,\
                        CONCAT(college.collegename, ' (', college.collegecode , ')') AS collegename\
                        FROM student\
                        JOIN course ON student.coursecode = course.coursecode\
                        JOIN college on course.collegecode = college.collegecode WHERE id = %s"
            cursor.execute(query, (student_id,))
            student_data = cursor.fetchone()
            if student_data:
                return student_data
            else:
                return None
        except Exception as e:
            raise e
        finally:
            cursor.close()