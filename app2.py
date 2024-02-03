from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Replace these placeholders with your MySQL server details
host = "localhost"
user = "root"
password = "Home@5095"
database = "information"

@app.route("/")
def index():
    return render_template("index2.html")

@app.route("/submit_data", methods=["POST"])
def submit_data():
    try:
        # Parse JSON data from the request
        data = request.get_json()

        # Connect to MySQL
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Insert data into the 'userdata' table
        insert_query = "INSERT INTO checkdata (email,password) VALUES (%s, %s)"
        data_values = (data['email'], data['password'])
        cursor.execute(insert_query, data_values)

        # Commit the changes
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return jsonify({"message": "Data submitted successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)