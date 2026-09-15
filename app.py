from flask import Flask, render_template, request

import sqlite3

# Create our Flask application
app = Flask(__name__)

# Create our database and table
def create_database():

    # Connect to the SQLite database
    # If the database doesn't exist, SQLite will create it
    connection = sqlite3.connect("database.db")

    # Create a cursor so we can execute SQL commands
    cursor = connection.cursor()

    # Create a table called users
    # IF NOT EXIST prevents an error if the table already exists
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,
                   surname TEXT
                   )
        """)
    
    # save the changes
    connection.commit()

    # Close the database connection
    connection.close()

@app.route("/")
def home():
    # Display out HTML page
    return render_template("index.html")

# Receive information from the HTLM form
@app.route("/submit", methods=["POST"])
def submit():

    # Get the name from the form
    name = request.form["name"]

    # Get the surname from the form
    surname = request.form["surname"]

    # Connect to our SQLite database
    connection = sqlite3.connect("database.db")

    # Create a cursor so we can execute SQL commands
    cursor = connection.cursor()

    cursor.execute(
            "INSERT INTO users(name, surname) VALUES(?,?)",
            (name,surname)
    )

    # save the changes
    connection.commit()

    # Close the database connection
    connection.close()



    # print the information in the terminal
    print(f"Your fullname {name} {surname}")

    # Send a response back to the browser
    return "Information saved succefully!"

if __name__ == "__main__":

    # Create the database before starting the app
    create_database()

    app.run(debug=True)

    