from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect("database.db")
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # ตารางพนักงาน
    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        emp_id TEXT PRIMARY KEY,
        name TEXT,
        department TEXT,
        position TEXT
    )
    """)

    # ตารางประวัติการเช็คอิน
    cur.execute("""
    CREATE TABLE IF NOT EXISTS checkin(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emp_id TEXT,
        time TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/checkin", methods=["POST"])
def checkin():

    emp_id = request.form["emp_id"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT name FROM employees WHERE emp_id=?", (emp_id,))
    emp = cur.fetchone()

    if emp is None:
        return "<h3>❌ ไม่พบรหัสพนักงาน</h3><a href='/'>กลับ</a>"

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("INSERT INTO checkin(emp_id,time,status) VALUES(?,?,?)",
                (emp_id,time,"Check-in"))

    conn.commit()
    conn.close()

    return redirect("/history")

@app.route("/checkout", methods=["POST"])
def checkout():

    emp_id = request.form["emp_id"]

    conn = get_db()
    cur = conn.cursor()

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("INSERT INTO checkin(emp_id,time,status) VALUES(?,?,?)",
                (emp_id,time,"Check-out"))

    conn.commit()
    conn.close()

    return redirect("/history")

@app.route("/add_employee")
def add_employee():
    return render_template("add_employee.html")

@app.route("/save_employee", methods=["POST"])
def save_employee():

    emp_id = request.form["emp_id"]
    name = request.form["name"]
    department = request.form["department"]
    position = request.form["position"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO employees VALUES (?,?,?,?)",
        (emp_id, name, department, position)
    )

    conn.commit()
    conn.close()

    return redirect("/employees")

@app.route("/history")
def history():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT checkin.id, employees.emp_id, employees.name, checkin.time, checkin.status
    FROM checkin
    JOIN employees ON employees.emp_id = checkin.emp_id
    ORDER BY checkin.id DESC
    """)

    data = cur.fetchall()

    conn.close()

    return render_template("history.html",data=data)

@app.route("/employees")
def employees():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()

    conn.close()

    return render_template("employees.html", data=data)

@app.route("/delete_employee/<emp_id>")
def delete_employee(emp_id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM checkin WHERE emp_id=?", (emp_id,))
    cur.execute("DELETE FROM employees WHERE emp_id=?", (emp_id,))

    conn.commit()
    conn.close()

    return redirect("/employees")
@app.route("/delete_history/<int:id>")
def delete_history(id):

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM checkin WHERE id=?", (id,))
    conn.commit()

    conn.close()

    return redirect("/history")


@app.route("/delete_all_history")
def delete_all_history():

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("DELETE FROM checkin")
    conn.commit()

    conn.close()

    return redirect("/history")

@app.route("/edit_employee/<emp_id>")
def edit_employee(emp_id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM employees WHERE emp_id=?", (emp_id,))
    emp = cur.fetchone()

    conn.close()

    return render_template("edit_employee.html", emp=emp)


@app.route("/update_employee", methods=["POST"])
def update_employee():

    emp_id = request.form["emp_id"]
    name = request.form["name"]
    department = request.form["department"]
    position = request.form["position"]

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    UPDATE employees
    SET name=?, department=?, position=?
    WHERE emp_id=?
    """,(name,department,position,emp_id))

    conn.commit()
    conn.close()

    return redirect("/employees")


if __name__ == "__main__":
    app.run(debug=True)