from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"  # required for session

# ==========================
# 🔐 ADMIN CREDENTIALS
# ==========================
# 👉 CHANGE THESE TO ANYTHING YOU WANT
ADMIN_USERNAME = "lavingston"
ADMIN_PASSWORD = "admin123"

# ==========================
# DATABASE CONNECTION
# ==========================
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT'))
    )

# ==========================
# LOGIN
# ==========================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 🔐 CHECK LOGIN
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

# ==========================
# DASHBOARD (PROTECTED)
# ==========================
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('students.html', students=students)

# ==========================
# ADD STUDENT
# ==========================
@app.route('/add', methods=['POST'])
def add_student():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    marks = request.form.get('marks')

    if not name or not age:
        return "Name and Age required!"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, age, grade, marks) VALUES (%s,%s,%s,%s)",
        (name, age, grade, marks)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

# ==========================
# UPDATE
# ==========================
@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    marks = request.form.get('marks')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET name=%s, age=%s, grade=%s, marks=%s WHERE id=%s",
        (name, age, grade, marks, id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

# ==========================
# DELETE
# ==========================
@app.route('/delete/<int:id>')
def delete_student(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('dashboard'))

# ==========================
# LOGOUT
# ==========================
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==========================
# RUN
# ==========================
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=10000)