import string
import random

from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Task 1", "done": False},
    {"id": 2, "title": "Task 2", "done": True},
]

urls_store = {}


# TODO add a thingy here to connect to a db using sqlite3, then read all of the info in from urls_store


def random_string():
    chs = string.ascii_letters + string.digits
    return "".join(random.choice(chs) for _ in range(5))


@app.route("/urls", methods=["GET"])
def get_urls():
    return jsonify({"urls": urls_store})


@app.route("/urls", methods=["POST"])
def create_url():
    if not request.json or "url" not in request.json:
        return jsonify({"Error": "URL shortener does not make sense"}), 400
    url_key = random_string()
    while url_key in urls_store.values():
        url_key = random_string()
    urls_store[request.json["url"]] = url_key
    print("URL storage = ", urls_store)
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
