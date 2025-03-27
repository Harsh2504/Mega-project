import mysql.connector

def get_db_connection():
    """
    Establishes and returns a connection to the database.
    """
    try:
        connection = mysql.connector.connect(
            host="gateway01.us-west-2.prod.aws.tidbcloud.com",
            port=4000,
            user="3vBMzU5RHaXD1tv.root",
            password="gSY9SiFI0JHWgiR2",
            database="systemdb",
            connection_timeout=300 # Set connection timeout to 300 seconds
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Database connection failed: {error}")
        return None

def test_db_connection():
    """
    Tests the database connection by fetching and printing all rows
    from the 'department' table.
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM department")
            departments = cursor.fetchall()

            print("Department data:")
            for department in departments:
                print(f"ID: {department[0]}, Name: {department[1]}, Description: {department[2]}")

            cursor.close()
        except mysql.connector.Error as error:
            print(f"Error while fetching data: {error}")
        finally:
            connection.close()
    else:
        print("Failed to establish a database connection.")

# Run the test function if this script is executed directly
if __name__ == "__main__":
    test_db_connection()