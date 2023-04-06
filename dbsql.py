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
