import string
import random
import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)
app.config["DATABASE"] = "urls.db"

tasks = [
    {"id": 1, "title": "Task 1", "done": False},
    {"id": 2, "title": "Task 2", "done": True},
]

urls_store = []
short_keys = set()


# TODO add a thingy here to connect to a db using sqlite3, then read all of the info in from urls_store
def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(app.config["DATABASE"])
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS urls (
        url_key TEXT NOT NULL,
        original_url TEXT NOT NULL,
        short_url TEXT NOT NULL
        )
        """
        )
        db.commit()
    return db


@app.teardown_appcontext
def db_down(e=None):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def random_string():
    chs = string.ascii_letters + string.digits
    return "".join(random.choice(chs) for _ in range(5))


def update_local_urls():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM urls")
    urls = cursor.fetchall()
    for url in urls:
        urls_store.append(
            {"url_key": url[0], "original_url": url[1], "short_url": url[2]}
        )
        short_keys.add(url[0])


@app.route("/urls", methods=["GET"])
def get_urls():
    if not urls_store:
        update_local_urls()
    return jsonify({"urls": urls_store})


@app.route("/urls", methods=["POST"])
def create_url():
    if not request.json or "url" not in request.json:
        return jsonify({"Error": "URL shortener does not make sense"}), 400
    url_key = random_string()
    while url_key in short_keys:
        url_key = random_string()
    urls_store.append(
        {
            "url_key": url_key,
            "original_url": request.url,
            "short_url": f"127.0.0.1:5000/{url_key}",
        }
    )
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        f"""INSERT into urls ("url_key", "original_url", "short_url") values (?,?,?)""",
        (url_key, request.url, f"127.0.0.1:5000/{url_key}"),
    )
    db.commit()
    return (
        jsonify(
            {
                "url_key": url_key,
                "original_url": request.json["url"],
                "short_url": f"127.0.0.1:5000/{url_key}",
            }
        ),
        201,
    )


@app.route("/tasks", methods=["POST"])
def create_task():
    if not request.json or "title" not in request.json:
        return jsonify({"error": "Title is required"}), 400

    new_task = {
        "id": tasks[-1]["id"] + 1,
        "title": request.json["title"],
        "done": False,
    }
    tasks.append(new_task)
    return jsonify({"task": new_task}), 201


if __name__ == "__main__":
    app.run(debug=True)
