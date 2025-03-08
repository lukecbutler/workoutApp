import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("workouts.db")
cursor = conn.cursor()

# Create the Workouts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Workouts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    exercise TEXT NOT NULL,
    sets INTEGER,
    reps INTEGER,
    weight REAL,
    duration REAL
);
''')
