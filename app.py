from flask import Flask, request, render_template, redirect, url_for
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Database connection
DATABASE = "workouts.db"

d
# Function to initialize the database
def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            exercise TEXT NOT NULL,
            sets INTEGER,
            reps INTEGER,
            weight REAL,
            duration REAL
        )
    ''')
    conn.commit()
    conn.close()

# Route: View all workout days and add a new day
@app.route("/", methods=["GET", "POST"])
def view_days():
    conn = get_db_connection()
    if request.method == "POST":
        date = request.form["date"]
        conn.close()
        return redirect(url_for("view_workouts_by_day", date=date))
    days = conn.execute("SELECT DISTINCT date FROM Workouts ORDER BY date DESC").fetchall()
    conn.close()
    return render_template("days.html", days=days)

# Route: View workouts for a specific day
@app.route("/day/<date>", methods=["GET", "POST"])
def view_workouts_by_day(date):
    conn = get_db_connection()
    if request.method == "POST":
        exercise = request.form["exercise"]
        sets = request.form.get("sets")
        reps = request.form.get("reps")
        weight = request.form.get("weight")
        duration = request.form.get("duration")
        conn.execute('''
            INSERT INTO Workouts (date, exercise, sets, reps, weight, duration)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, exercise, sets, reps, weight, duration))
        conn.commit()
    workouts = conn.execute("SELECT * FROM Workouts WHERE date = ?", (date,)).fetchall()
    conn.close()
    return render_template("workouts.html", date=date, workouts=workouts)

# Route: Delete a workout
@app.route("/delete/<int:id>/<date>", methods=["POST"])
def delete_workout(id, date):
    conn = get_db_connection()
    conn.execute("DELETE FROM Workouts WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("view_workouts_by_day", date=date))

# Route: Update a workout
@app.route("/update/<int:id>/<date>", methods=["GET", "POST"])
def update_workout(id, date):
    conn = get_db_connection()
    workout = conn.execute("SELECT * FROM Workouts WHERE id = ?", (id,)).fetchone()
    if request.method == "POST":
        exercise = request.form["exercise"]
        sets = request.form.get("sets")
        reps = request.form.get("reps")
        weight = request.form.get("weight")
        duration = request.form.get("duration")
        conn.execute('''
            UPDATE Workouts
            SET exercise = ?, sets = ?, reps = ?, weight = ?, duration = ?
            WHERE id = ?
        ''', (exercise, sets, reps, weight, duration, id))
        conn.commit()
        conn.close()
        return redirect(url_for("view_workouts_by_day", date=date))
    conn.close()
    return render_template("update.html", workout=workout, date=date)

# Main function
if __name__ == "__main__":
    initialize_db()
    app.run(debug=True, port=80, host="0.0.0.0")