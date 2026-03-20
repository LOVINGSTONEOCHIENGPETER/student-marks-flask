from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# DATABASE CONNECTION
def get_db_connection():
    return mysql.connector.connect(
        host='ballast.proxy.rlwy.net',
        user='root',
        password='YOUR_PASSWORD',
        database='railway',
        port=53565
    )

# HOME PAGE (GET)
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('students.html', students=students)

# ADD STUDENT (POST)
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    marks = request.form.get('marks')

    if not name or not age:
        return "Name and Age required!"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, age, grade, marks) VALUES (%s, %s, %s, %s)",
        (name, age, grade, marks)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

# DELETE
@app.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

# UPDATE
@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):
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

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)