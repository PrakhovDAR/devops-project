import subprocess
from pathlib import Path

ROOT = Path("/opt/project")

EXPECTED_MESSAGES = (
    "missing-module-docstring",
    "missing-function-docstring",
    "invalid-name",
    "dangerous-default-value",
    "unused-variable",
    "singleton-comparison",
    "bare-except",
    "consider-using-with",
    "unspecified-encoding",
    "unreachable",
)


def test_pylint_finds_all_required_static_analysis_criteria():
    result = subprocess.run(
        [
            "pylint",
            "--rcfile",
            str(ROOT / "tester" / "pylintrc"),
            str(ROOT / "app" / "app.py"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    output = result.stdout + result.stderr
    assert result.returncode != 0, "pylint should find intentionally added violations"
    for message in EXPECTED_MESSAGES:
        assert message in output
