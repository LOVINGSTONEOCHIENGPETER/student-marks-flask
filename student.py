from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages

# ---------------- Database connection ---------------- #
def db_connection():
    # Replace with your PlanetScale credentials
    conn = mysql.connector.connect(
        host="your-planetscale-host",       # e.g., us-east.connect.psdb.io
        user="your-username",               # PlanetScale username
        password="your-password-or-token",  # PlanetScale password or token
        database="elimu_predict_online"     # Your PlanetScale database
        # ssl_disabled=True                 # Uncomment if testing without SSL (not recommended)
    )
    return conn

# ---------------- Add student route ---------------- #
@app.route("/", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        id_ = request.form.get("id")
        name = request.form.get("name")
        math = request.form.get("math")
        english = request.form.get("english")
        science = request.form.get("science")
        social = request.form.get("social")
        kiswahili = request.form.get("kiswahili")

        # Validation
        if not all([id_, name, math, english, science, social, kiswahili]):
            flash("All fields are required!", "error")
            return redirect(url_for("add_student"))

        try:
            # Convert numeric fields
            id_ = int(id_)
            math = int(math)
            english = int(english)
            science = int(science)
            social = int(social)
            kiswahili = int(kiswahili)
        except ValueError:
            flash("ID and scores must be numbers!", "error")
            return redirect(url_for("add_student"))

        try:
            con = db_connection()
            cursor = con.cursor()
            sql = """INSERT INTO students 
                     (id, name, math, english, science, social, kiswahili)
                     VALUES (%s,%s,%s,%s,%s,%s,%s)"""
            cursor.execute(sql, (id_, name, math, english, science, social, kiswahili))
            con.commit()
            cursor.close()
            con.close()
            flash(f"Student {name} added successfully!", "success")
        except mysql.connector.errors.IntegrityError:
            flash(f"Student with ID {id_} already exists!", "error")
        except Exception as e:
            flash(f"Database error: {str(e)}", "error")

        return redirect(url_for("add_student"))

    # GET request
    return render_template("students.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)