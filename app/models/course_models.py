from app import mysql

class course_model:
    @classmethod    
    def delete_course(cls, coursecode):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to delete a course by course code
            delete_query = "DELETE FROM course WHERE coursecode = %s"
            
            # Execute the query with the course code
            cursor.execute(delete_query, (coursecode,))
            
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
    def update_course(cls, course_data):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to update an existing course
            update_query = "UPDATE course SET coursename = %s, collegecode = %s WHERE coursecode = %s"
            print(update_query)
            print(course_data)
            # Execute the query with the course data
            cursor.execute(update_query, (course_data['coursename'], course_data['collegecode'], course_data['coursecode']))
            
            # Commit the transaction to save the changes to the database
            connection.commit()

        except Exception as e:
            # Handle any errors that may occur during the update
            connection.rollback()
            raise e
        finally:
            cursor.close()

    @classmethod
    def create_course(cls, course_data):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to insert a new course
            insert_query = "INSERT INTO course (coursecode, coursename, collegecode) VALUES (%s, %s, %s)"
            
            # Execute the query with the course data
            cursor.execute(insert_query, (course_data['coursecode'], course_data['coursename'], course_data['collegecode']))
            
            # Commit the transaction to save the changes to the database
            connection.commit()

        except Exception as e:
            # Handle any errors, such as duplicate course codes
            connection.rollback()
            raise e
        finally:
            cursor.close()

    @classmethod
    def get_courses(cls):
        connection = mysql.connection
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM course')
        data = cursor.fetchall()
        cursor.close()
        return data