import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load environment variables
load_dotenv()

# Connect to database
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

print("="*60)
print("PASSWORD RESET UTILITY")
print("="*60)

# Show all users
cursor = mydb.cursor()
cursor.execute("SELECT id, email, name, post FROM users ORDER BY id")
users = cursor.fetchall()

print("\nCurrent users in database:")
print("-" * 60)
for user in users:
    print(f"ID: {user[0]:<5} | Email: {user[1]:<30} | Name: {user[2]:<20} | Role: {user[3]}")
print("-" * 60)

# Get user email to reset
email = input("\nEnter the email address of the user to reset password: ").strip()

# Verify user exists
cursor.execute("SELECT id, name FROM users WHERE email = %s", (email,))
user = cursor.fetchone()

if not user:
    print(f"\n❌ User with email '{email}' not found!")
    mydb.close()
    exit(1)

print(f"\nFound user: {user[1]} (ID: {user[0]})")

# Get new password
new_password = input("Enter new password: ").strip()
confirm_password = input("Confirm password: ").strip()

if new_password != confirm_password:
    print("\n❌ Passwords don't match!")
    mydb.close()
    exit(1)

if len(new_password) < 4:
    print("\n❌ Password must be at least 4 characters!")
    mydb.close()
    exit(1)

# Hash the password
hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

print(f"\nHashed password: {hashed_password[:50]}...")

# Confirm update
confirm = input(f"\nUpdate password for {user[1]} ({email})? (yes/no): ").strip().lower()

if confirm != 'yes':
    print("\n❌ Operation cancelled.")
    mydb.close()
    exit(0)

# Update password
cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
mydb.commit()

print(f"\n✅ Password updated successfully for {email}")
print(f"You can now login with:")
print(f"  Email: {email}")
print(f"  Password: {new_password}")

cursor.close()
mydb.close()
