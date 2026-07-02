import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)
DB_FILE = "courses.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                code TEXT UNIQUE NOT NULL
            )
        """)
        try:
            conn.execute("INSERT INTO courses (id, name, code) VALUES (1, 'Cloud Native Frameworks', 'CS-10')")
            conn.commit()
        except sqlite3.IntegrityError:
            pass

@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, code FROM courses WHERE id = ?", (course_id,))
        row = cursor.fetchone()
    if not row:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({"id": row[0], "name": row[1], "code": row[2]}), 200

if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)