from werkzeug.security import check_password_hash

# Test the hashed password from your database
stored_hash = "pbkdf2:sha256:260000$5YJ8AFHEIAFqsnGb$5ecd2b34e49c73dd517b99e8dc4c3f4eb705d4327db291edb5a90a6dc3c0c71a"

# Test with different passwords to find which one works
test_passwords = [
    "admin",
    "Admin",
    "password",
    "Password",
    "123456",
    # Add the password you think it should be
]

print(f"Testing hash: {stored_hash}\n")
print(f"Hash starts with 'pbkdf2:sha256:': {stored_hash.startswith('pbkdf2:sha256:')}\n")

for pwd in test_passwords:
    result = check_password_hash(stored_hash, pwd)
    print(f"Password '{pwd}': {result}")

print("\n" + "="*50)
print("Enter the actual password to test:")
actual_password = input("> ")
if actual_password:
    result = check_password_hash(stored_hash, actual_password)
    print(f"\nPassword '{actual_password}': {result}")
