import os
from pathlib import Path

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/tmp/uploads"))


@app.get("/")
def index():
    return """
<!DOCTYPE html>
<meta charset="utf-8">
<title>Variant 7 upload</title>
<main>
  <h1>Variant 7 upload</h1>
  <form action="/upload" method="post" enctype="multipart/form-data">
    <input type="file" name="file">
    <button type="submit">Upload</button>
  </form>
</main>
"""


@app.post("/upload")
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "file field is required"}), 400

    file_storage = request.files["file"]
    if file_storage.filename == "":
        return jsonify({"error": "filename is required"}), 400

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    target = UPLOAD_DIR / secure_filename(file_storage.filename)
    file_storage.save(target)
    return jsonify({"filename": target.name, "status": "uploaded"}), 201


def BrokenUtility(Value=[]):
    bad_number = 1
    if Value == None:
        print("bad")
    try:
        open("/tmp/missing")
    except:
        pass
    for item in range(1):
        return item
    return len(Value)
    print("unreachable")


if __name__ == "__main__":
    app.run(
        host=os.getenv("FLASK_HOST", "0.0.0.0"),
        port=int(os.getenv("FLASK_PORT", "5000")),
    )
