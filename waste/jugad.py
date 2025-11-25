import mysql.connector

try:
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database="feedback"
    )
    print("Connection successful!")
    
    # Get a cursor to execute SQL queries
    cursor = mydb.cursor()

    # Fetch all the data from the department table
    cursor.execute("SELECT * FROM department")
    departments = cursor.fetchall()

    # Print the department data
    print("Department data:")
    for department in departments:
        print("ID: {}, Name: {}, Description: {}".format(department[0], department[1], department[2]))

    # Close the cursor and database connection
    cursor.close()
    mydb.close()

except mysql.connector.Error as error:
    print("Connection failed! {}".format(error))
