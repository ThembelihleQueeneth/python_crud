from flask import Flask, render_template, request, redirect

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

    connection = sqlite3.connect("database.db")

    cursor = connection.cursor()

    # Get all the usets from the database

    cursor.execute("SELECT *FROM users")

    # Store the results in the users variables
    users = cursor.fetchall()

    # Close the database connection
    connection.close()

    # Send the users to our HTLM page
    return render_template("index.html", users=users)

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
    return redirect("/")

@app.route("/delete/<int:user_id>", methods=["POST"])
def delete(user_id):
    # Connect to our SQLite database
    connection = sqlite3.connect("database.db")

    # Create a cursor so we can execute SQL commands
    cursor = connection.cursor()

    # Delete the user with the matching ID
    cursor.execute(
        "DELETE FROM users WHERE id = ?",(user_id,)
    )

    # Save the changes
    connection.commit()

    # Close the database connection
    connection.close()

    # Retun to the home page
    return redirect("/")

@app.route("/edit/<int:user_id>")
def edit(user_id):
     # Connect to our SQLite database
    connection = sqlite3.connect("database.db")

    # Create a cursor so we can execute SQL commands
    cursor = connection.cursor()

    # Find the uer with the matching ID
    cursor.execute(
        "SELECT *FRO< users WHERE id=?",
        (user_id)
    )

    # Get the user's information
    user = cursor.fetchone()

    # Close the database connection
    connection.close()

    # Retun to the home page
    return render_template("edit.html",user=user)

@app.route("/update/<int:user_id>", methods=["POST"])
def update(user_id):

    # Get the new name from the form
    name = request.form["name"]

    # Get the new surname from the form
    surname = request.form["surname"]

    # Connect to our SQLite database
    connection = sqlite3.connect("database.db")

    # Create a cursor so we can execute SQL commands
    cursor = connection.cursor()

    # Update the user's information
    cursor.execute(
        "UPDATE users SET name = ?, surname = ? WHERE id = ?",
        (name, surname, user_id)
    )

    # Save the changes
    connection.commit()

    # Close the database connection
    connection.close()

    return redirect("/")



if __name__ == "__main__":

    # Create the database before starting the app
    create_database()

    app.run(debug=True)

    
