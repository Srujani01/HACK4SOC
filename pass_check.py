import mysql.connector

# Replace these placeholders with your MySQL server details
userdata_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Home@5095',
    'database': 'information'
}

checkdata_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Home@5095',
    'database': 'information'
}

def compare_passwords():
    try:
        # Connect to the userdata database
        userdata_conn = mysql.connector.connect(**userdata_config)
        userdata_cursor = userdata_conn.cursor()

        # Connect to the checkdata database
        checkdata_conn = mysql.connector.connect(**checkdata_config)
        checkdata_cursor = checkdata_conn.cursor()

        # Fetch email and password from userdata
        userdata_cursor.execute("SELECT email, password FROM userdata")
        userdata_results = userdata_cursor.fetchall()

        for email, password_userdata in userdata_results:
            # Fetch password from checkdata for the same email
            checkdata_cursor.execute("SELECT password FROM checkdata WHERE email = %s", (email,))
            checkdata_result = checkdata_cursor.fetchone()

            if checkdata_result:
                password_checkdata = checkdata_result[0]

                # Compare passwords
                if password_userdata == password_checkdata:
                    print(f"Passwords match for email: {email}")
                else:
                    print(f"Passwords do not match for email: {email}")
            else:
                print(f"No entry found in checkdata for email: {email}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close database connections
        if userdata_conn.is_connected():
            userdata_cursor.close()
            userdata_conn.close()

        if checkdata_conn.is_connected():
            checkdata_cursor.close()
            checkdata_conn.close()

if __name__ == "__main__":
    compare_passwords()
