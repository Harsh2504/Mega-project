"""
Password Migration Script
=========================
This script migrates existing plain text passwords to hashed passwords.

IMPORTANT: 
1. Backup your database before running this script!
2. Run this script only once
3. After running, all users will need to use their original passwords (they will be hashed)
"""

import mysql.connector
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_passwords():
    """Migrate all plain text passwords to hashed passwords."""
    
    print("🔐 Password Migration Script")
    print("=" * 50)
    
    # Confirm with user
    confirm = input("\n⚠️  WARNING: This will modify all user passwords in the database.\n"
                   "Have you backed up your database? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Migration cancelled. Please backup your database first.")
        return
    
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            connection_timeout=300
        )
        
        cursor = connection.cursor()
        
        # Get all users with their passwords
        cursor.execute("SELECT id, email, password FROM users")
        users = cursor.fetchall()
        
        print(f"\n📊 Found {len(users)} users to migrate")
        
        migrated = 0
        skipped = 0
        
        for user in users:
            user_id, email, plain_password = user
            
            # Check if password is already hashed
            if plain_password.startswith('pbkdf2:sha256:') or plain_password.startswith('scrypt:'):
                print(f"⏭️  Skipping {email} - already hashed")
                skipped += 1
                continue
            
            # Hash the password
            hashed_password = generate_password_hash(plain_password, method='pbkdf2:sha256')
            
            # Update the user record
            cursor.execute(
                "UPDATE users SET password=%s WHERE id=%s", 
                (hashed_password, user_id)
            )
            
            print(f"✅ Migrated {email}")
            migrated += 1
        
        # Commit changes
        connection.commit()
        
        print("\n" + "=" * 50)
        print(f"✨ Migration Complete!")
        print(f"   Migrated: {migrated} users")
        print(f"   Skipped: {skipped} users (already hashed)")
        print(f"   Total: {len(users)} users")
        print("\n⚠️  Important: Users can still login with their original passwords.")
        print("   The passwords are now securely hashed in the database.")
        
    except mysql.connector.Error as error:
        print(f"\n❌ Database error: {error}")
        connection.rollback()
    
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    migrate_passwords()
