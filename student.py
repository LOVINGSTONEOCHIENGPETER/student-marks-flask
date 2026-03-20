from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='ballast.proxy.rlwy.net',
        user='root',
        password='cMWpCHeUcTiBBVTwUrQrbkRuSNLdFRsQ',
        database='railway',
        port=53565
    )
    return conn

# Home / View all students
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)

# Add student
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    marks = request.form.get('marks')

    if not name or not age:
        return "Name and Age are required!", 400

    try:
        age = int(age)
        marks = int(marks) if marks else None
    except ValueError:
        return "Age and Marks must be numbers!", 400

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

# Update student
@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):
    name = request.form.get('name')
    age = request.form.get('age')
    grade = request.form.get('grade')
    marks = request.form.get('marks')

    if not name or not age:
        return "Name and Age are required!", 400

    try:
        age = int(age)
        marks = int(marks) if marks else None
    except ValueError:
        return "Age and Marks must be numbers!", 400

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

# Delete student
@app.route('/delete/<int:id>', methods=['GET'])
def delete_student(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)