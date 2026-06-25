import os
import time

import requests


def test_file_upload_returns_created_status_and_filename():
    url = os.getenv("APP_URL", "http://app:5000")
    upload_name = os.getenv("UPLOAD_FILE_NAME", "variant7.txt")
    for _ in range(30):
        try:
            requests.get(url, timeout=1)
            break
        except requests.RequestException:
            time.sleep(1)
    else:
        raise AssertionError("app did not become available")

    files = {"file": (upload_name, b"variant 7 integration upload\n", "text/plain")}
    response = requests.post(f"{url}/upload", files=files, timeout=5)
    assert response.status_code == 201
    assert response.json().get("filename") == upload_name
