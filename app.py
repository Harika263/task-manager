from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

# Create tables
def init_db():
    db = get_db()
    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT, user TEXT)")
    db.commit()

init_db()

@app.route('/')
def home():
    if "user" in session:
        db = get_db()
        tasks = db.execute("SELECT * FROM tasks WHERE user=?", (session["user"],)).fetchall()
        return render_template("dashboard.html", tasks=tasks)
    return redirect("/login")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()
        db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
        db.commit()

        return redirect("/login")
    
    return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()
        result = db.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd)).fetchone()

        if result:
            session["user"] = user
            return redirect("/")
        else:
            return "Invalid Credentials ❌"

    return render_template("login.html")

@app.route('/add', methods=["POST"])
def add_task():
    task = request.form["task"]
    db = get_db()
    db.execute("INSERT INTO tasks (task, user) VALUES (?, ?)", (task, session["user"]))
    db.commit()
    return redirect("/")

@app.route('/delete/<int:id>')
def delete_task(id):
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id=?", (id,))
    db.commit()
    return redirect("/")

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)