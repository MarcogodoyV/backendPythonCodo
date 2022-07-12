from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")

app.config["MYSQL_HOST"] = HOST
app.config["MYSQL_USER"] = USER
app.config["MYSQL_PASSWORD"] = PASSWORD
app.config["MYSQL_DB"] = "sql10505778"

mysql = MySQL(app)


@app.route("/api/tasks", methods=["GET", "POST"])
def getTasks():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("Select * from tasks")
        results = cur.fetchall()
        cur.close()
        tasks = []
        for result in results:
            task = {
                "id": result[0],
                "title": result[1],
                "description": result[2],
                "pomodoros": result[3],
                "taskDone": result[4],
            }
            tasks.append(task)
        return jsonify(tasks)
    elif request.method == "POST":
        print(request.json)
        if request.json["title"] != "" or request.json["description"] != "":
            new_task = {
                "title": request.json["title"],
                "description": request.json["description"],
                "pomodoros": int(
                    request.json["pomodoros"] if request.json["pomodoros"] != "" else 0
                ),
            }
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO tasks (title,description,pomodoros, taskDone) VALUES (%s,%s,%s,0)",
                (
                    new_task["title"],
                    new_task["description"],
                    new_task["pomodoros"],
                ),
            )
            mysql.connection.commit()
            cur.close()

            return jsonify({"message": "Task added to List"})
        else:
            return jsonify({"message": " Task not added to list"})


@app.route("/api/tasks/<int:id>", methods=["GET"])
def getTask(id):
    cur = mysql.connection.cursor()
    cur.execute(f"select * from tasks where id = '{id}'")
    result = cur.fetchone()
    cur.close()
    print(result)
    return jsonify(result)


# falta este
@app.route("/api/tasks/<int:id>", methods=["PUT"])
def editTask(id):
    print(id)
    print(request.json["title"])
    cur = mysql.connection.cursor()
    cur.execute(
        f'update tasks set title="{request.json["title"]}", description="{request.json["description"]}", pomodoros={request.json["pomodoros"]}, taskDone={request.json["taskDone"]} where id={id}'
    )
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Task edited"})


@app.route("/api/tasks/<int:id>", methods=["DELETE"])
def deleteTask(id):
    cur = mysql.connection.cursor()
    cur.execute(f"delete from tasks where id ='{id}'")
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Task deleted"})


@app.route("/api/tasks/all", methods=["DELETE"])
def deleteTasksAll():
    cur = mysql.connection.cursor()
    cur.execute("delete from tasks")
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=4000)
