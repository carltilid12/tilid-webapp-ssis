from app import mysql

class college_model:
    @classmethod
    def create_college(cls, college_data):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to insert a new college
            insert_query = "INSERT INTO college (collegecode, collegename) VALUES (%s, %s)"

            # Execute the query with the college data
            cursor.execute(insert_query, (college_data['collegecode'], college_data['collegename']))

            # Commit the transaction to save the changes to the database
            connection.commit()

        except Exception as e:
            # Handle any errors, such as duplicate college codes
            connection.rollback()
            raise e
        finally:
            cursor.close()

    @classmethod
    def get_colleges(cls):
        connection = mysql.connection
        cursor = connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM college')
        data = cursor.fetchall()
        cursor.close()
        return data