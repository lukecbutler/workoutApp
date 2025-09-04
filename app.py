from flask import Flask, request, render_template, redirect, url_for
import sqlite3

# Initialize Flask app
app = Flask(__name__)

# Database connection
DATABASE = "workouts.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Route: View all workout days and add a new day
@app.route("/", methods=["GET", "POST"])
def view_days():
    conn = get_db_connection()
    if request.method == "POST":
        date = request.form["date"]
        print(date)
        conn.close()
        return redirect(url_for("view_workouts_by_day", date=date))
    days = conn.execute("SELECT DISTINCT date FROM Workouts ORDER BY date DESC").fetchall()
    conn.close()

    return render_template("mainpage.html", days = days)

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


# Route: View workout timeline for 2025
@app.route("/liftingSchedule2025", methods=["GET", "POST"])
def liftingSchedule2025():
    return render_template("liftingSchedule2025.html")


# Route: View workout timeline for 1/25
@app.route("/janurary25", methods=["GET", "POST"])
def janurary2025():
    return render_template("janurary2025.html")

# Route: View workout timeline for 2/25
@app.route("/feburary25", methods=["GET", "POST"])
def feburary2025():
    return render_template("feburary2025.html")

# Route: View workout timeline for 3/25
@app.route("/march25", methods=["GET", "POST"])
def march2025():
    return render_template("march2025.html")

# Main function
if __name__ == "__main__":
    app.run(debug=True)