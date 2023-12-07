import mysql.connector

# Connect to MySQL Server
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sfsys123"
)

# Create a new database
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE SystemDB")

# Use SystemDB database
mycursor.execute("USE SystemDB")

# Create Users table
mycursor.execute("CREATE TABLE Users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")

# Create Department table
mycursor.execute("CREATE TABLE Department (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), location VARCHAR(255))")

# Create Class table
mycursor.execute("CREATE TABLE Class (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), teacher VARCHAR(255))")

# Create Division table
mycursor.execute("CREATE TABLE Division (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description VARCHAR(255))")

# Close the database connection
mydb.close()


#CREATE VIEW sgp AS
#SELECT
#    teach_id,
#    AVG(q1) AS q1,
#    AVG(q2) AS q2,
#    AVG(q3) AS q3,
#    AVG(q4) AS q4,
#    AVG(q5) AS q5,
#    AVG(q6) AS q6,
#    AVG(q7) AS q7,
#    AVG(q8) AS q8,
#    AVG(q9) AS q9,
#    AVG(q10) AS q10,
#    AVG(avg) AS avg
#FROM
#    feedbacknew
#GROUP BY
#    teach_id;
