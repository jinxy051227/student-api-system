from flask import Flask, jsonify, request
import json

app = Flask(__name__)

DATA_FILE = "students.json"


def load_students():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_students(students):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(students, f, indent=2)


@app.route("/")
def home():
    return "Student API System is running."


@app.route("/students", methods=["GET"])
def get_students():
    students = load_students()
    return jsonify(students)


@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    students = load_students()
    for student in students:
        if student["id"] == student_id:
            return jsonify(student)
    return jsonify({"error": "Student not found"}), 404


@app.route("/students", methods=["POST"])
def add_student():
    students = load_students()
    new_student = request.get_json()

    if not new_student:
        return jsonify({"error": "No data provided"}), 400

    students.append(new_student)
    save_students(students)

    return jsonify({"message": "Student added successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)