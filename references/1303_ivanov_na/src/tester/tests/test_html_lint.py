import subprocess
from pathlib import Path

APP_DIR = Path("/opt/project/app")


def test_upload_template_passes_html_linter():
    result = subprocess.run(
        ["html_lint.py", str(APP_DIR / "templates" / "upload.html")],
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
