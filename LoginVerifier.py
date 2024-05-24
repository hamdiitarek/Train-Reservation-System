import sys
sys.dont_write_bytecode = True

import CreateConnection
import bcrypt

def create_user(username, hashed_password, salt):
    # Insert the new user into the database
    connection = CreateConnection.create()
    backEnd = connection.cursor()
    
    sql = "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s)"
    val = (username, hashed_password, salt)
    backEnd.execute(sql, val)
    connection.commit()
    
    backEnd.close()
    connection.close()
    return True  # Indicate successful registration

# Hash and store password
def hash_password(password):
    salt = bcrypt.gensalt()  # Generate a random salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)  # Hash the password with the salt
    return hashed_password, salt

# Verify password
def verify_password(password, hashed_password, salt):
    salt_bytes = salt.encode('utf-8')  # Convert the salt to a byte string
    input_hash = bcrypt.hashpw(password.encode('utf-8'), salt_bytes)  # Hash the input password with the stored salt
    return input_hash == hashed_password.encode()  # Convert the stored hashed password to a byte string before comparing


if __name__ == "__main__":
    # Create a new user
    
    # Retrieve hashed password and salt from database
    connection = CreateConnection.create()
    backEnd = connection.cursor()
    sql = "SELECT password_hash, salt FROM users WHERE username = %s"
    val = ("admin",)
    backEnd.execute(sql, val)
    result = backEnd.fetchone()
    if result:
        stored_hashed_password, stored_salt = result
        print(verify_password("admin", stored_hashed_password, stored_salt))
    else:
        print("User not found")
        exit(1)
    backEnd.close()
    connection.close()
