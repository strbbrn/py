import mysql.connector
import hashlib

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="shashi"
)
def register_user(data):
    cursor = db.cursor()
    email = data['email']
    password = data['password']
    hashed_password = hashlib.md5(password.encode()).hexdigest()
    cursor.execute("INSERT INTO admin (email, password) VALUES (%s, %s)",
                   (email, hashed_password))
    db.commit()
    cursor.close()


def db_login(email):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admin WHERE email = %s", (email,))
    user = cursor.fetchone()
    return user

def get_all_students():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.close()
    return students

def get_student_by_id(user_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

def create_student(name, email):
    cursor = db.cursor()
    cursor.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
    db.commit()
    print(cursor.rowcount)
    cursor.close()

def update_student(user_id, name, email):
    cursor = db.cursor()
    cursor.execute("UPDATE students SET name = %s, email = %s WHERE id = %s", (name, email, user_id))
    db.commit()
    print(cursor.rowcount)
    count = cursor.rowcount
    cursor.close()
    return count

def delete_student(user_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (user_id,))
    db.commit()
    print(cursor.rowcount)
    count = cursor.rowcount
    cursor.close()
    return count
