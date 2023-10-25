from app import mysql

class college_model:
    @classmethod
    def delete_college(cls, collegecode):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to delete a college by college code
            delete_query = "DELETE FROM college WHERE collegecode = %s"

            # Execute the query with the college code
            cursor.execute(delete_query, (collegecode,))

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
    def update_college(cls, college_data):
        connection = mysql.connection
        cursor = connection.cursor()
        try:
            # Define the SQL query to update an existing college
            update_query = "UPDATE college SET collegename = %s WHERE collegecode = %s"
            print(update_query)
            print(college_data)
            # Execute the query with the college data
            cursor.execute(update_query, (college_data['collegename'], college_data['collegecode']))
            
            # Commit the transaction to save the changes to the database
            connection.commit()

        except Exception as e:
            # Handle any errors that may occur during the update
            connection.rollback()
            raise e
        finally:
            cursor.close()
            
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