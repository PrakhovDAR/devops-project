"""
Integration tests for EXAMPLE_APP endpoints.
Uses the requests library to verify HTTP status codes.
The app URL is read from APP_HOST / APP_INTERNAL_PORT env-vars.
"""
import os

import pytest
import requests

APP_HOST = os.environ.get("APP_HOST", "app")
APP_PORT = os.environ.get("APP_INTERNAL_PORT", "5000")
BASE_URL = f"http://{APP_HOST}:{APP_PORT}"


def _get(path: str, allow_redirects: bool = True, **kwargs) -> requests.Response:
    return requests.get(
        f"{BASE_URL}{path}",
        allow_redirects=allow_redirects,
        timeout=10,
        **kwargs,
    )


def _post(path: str, **kwargs) -> requests.Response:
    return requests.post(
        f"{BASE_URL}{path}",
        allow_redirects=False,
        timeout=10,
        **kwargs,
    )


class TestIndexEndpoint:
    """Tests for GET /"""

    def test_index_returns_200(self):
        """GET / must return HTTP 200."""
        response = _get("/")
        assert response.status_code == 200, (
            f"Expected 200 from GET /, got {response.status_code}"
        )


class TestUploadEndpoint:
    """Tests for GET /upload"""

    def test_upload_get_returns_200(self):
        """GET /upload must return HTTP 200 (the upload form)."""
        response = _get("/upload")
        assert response.status_code == 200, (
            f"Expected 200 from GET /upload, got {response.status_code}"
        )


class TestFilesEndpoint:
    """Tests for GET /files"""

    def test_files_returns_200(self):
        """GET /files must return HTTP 200."""
        response = _get("/files")
        assert response.status_code == 200, (
            f"Expected 200 from GET /files, got {response.status_code}"
        )


class TestToFilesEndpoint:
    """Tests for the /to_files redirect endpoint."""

    def test_to_files_redirects(self):
        """GET /to_files without following redirects must return 302."""
        response = _get("/to_files", allow_redirects=False)
        assert response.status_code == 302, (
            f"Expected 302 from GET /to_files, got {response.status_code}"
        )


class TestSuccessEndpoint:
    """Tests for GET /success/<name>"""

    def test_success_returns_200(self):
        """GET /success/testuser must return HTTP 200."""
        response = _get("/success/testuser")
        assert response.status_code == 200, (
            f"Expected 200 from GET /success/testuser, got {response.status_code}"
        )

    def test_success_contains_name(self):
        """Response body must contain the provided name."""
        response = _get("/success/alice")
        assert "alice" in response.text, (
            f'Expected name "alice" in /success/alice response, got: {response.text[:200]}'
        )


class TestIncrementEndpoint:
    """Tests for GET /increment/<int:a>"""

    def test_increment_redirects(self):
        """GET /increment/1 without following redirects must return 302."""
        response = _get("/increment/1", allow_redirects=False)
        assert response.status_code == 302, (
            f"Expected 302 from GET /increment/1 (no follow), got {response.status_code}"
        )


class TestOddEndpoint:
    """Tests for GET /odd/<int:a>"""

    def test_odd_returns_200(self):
        """GET /odd/3 must return HTTP 200."""
        response = _get("/odd/3")
        assert response.status_code == 200, (
            f"Expected 200 from GET /odd/3, got {response.status_code}"
        )

    def test_odd_contains_number(self):
        """Response must contain the number."""
        response = _get("/odd/7")
        assert "7" in response.text, (
            f'Expected "7" in /odd/7 response, got: {response.text[:200]}'
        )


class TestCheckEvenEndpoint:
    """Tests for GET /check_even/<int:a>"""

    def test_check_even_redirects(self):
        """GET /check_even/4 without following redirects must return 302."""
        response = _get("/check_even/4", allow_redirects=False)
        assert response.status_code == 302, (
            f"Expected 302 from GET /check_even/4, got {response.status_code}"
        )

    def test_check_odd_redirects(self):
        """GET /check_even/3 without following redirects must return 302."""
        response = _get("/check_even/3", allow_redirects=False)
        assert response.status_code == 302, (
            f"Expected 302 from GET /check_even/3, got {response.status_code}"
        )


class TestLoginEndpoint:
    """Tests for POST /login"""

    def test_login_wrong_credentials_returns_401(self):
        """POST /login with wrong credentials must return HTTP 401."""
        response = _post("/login", data={"name": "hacker", "password": "wrong"})
        assert response.status_code == 401, (
            f"Expected 401 from POST /login with bad creds, got {response.status_code}"
        )

    def test_login_correct_credentials_redirects(self):
        """POST /login with correct credentials must return 302 redirect."""
        response = _post("/login", data={"name": "admin", "password": "password"})
        assert response.status_code == 302, (
            f"Expected 302 from POST /login with correct creds, got {response.status_code}"
        )


class TestDownloadEndpoint:
    """Tests for GET /download/<name>"""

    def test_download_nonexistent_returns_404(self):
        """GET /download/nonexistent_file.txt must return HTTP 404."""
        response = _get("/download/nonexistent_file_xyz_12345.txt")
        assert response.status_code == 404, (
            f"Expected 404 from GET /download/nonexistent_file.txt, got {response.status_code}"
        )
