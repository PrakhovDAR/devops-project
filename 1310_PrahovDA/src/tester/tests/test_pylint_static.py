"""
Static analysis tests.

Stage 1 - YAPF:
    Checks that EXAMPLE_APP Python source files have formatting issues.
    The test FAILS (raises AssertionError) when YAPF produces a non-empty diff,
    because the CI pipeline must reject badly-formatted code.

Stage 2 - Pylint:
    Verifies that Pylint finds all 10 configured error codes in bad_code.py.
    The test FAILS when Pylint exits with code 0 (no errors found), because
    bad_code.py is intentionally broken and must always fail the linter.
"""
import os
import subprocess
import sys

import pytest

# ---------------------------------------------------------------------------
# Paths (resolved relative to this file so tests work from any cwd)
# ---------------------------------------------------------------------------
_TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
_TESTER_DIR = os.path.dirname(_TESTS_DIR)

BAD_CODE_PATH = os.path.join(_TESTER_DIR, "bad_code.py")
PYLINTRC_PATH = os.path.join(_TESTER_DIR, "pylintrc")

# Directory that contains the EXAMPLE_APP Python sources for YAPF analysis.
# Injected via env-var so that both local runs and Docker runs work.
APP_SRC_DIR = os.environ.get("APP_SRC_DIR", "/app")


# ---------------------------------------------------------------------------
# YAPF tests
# ---------------------------------------------------------------------------
def _collect_py_files(directory: str) -> list:
    """Return a sorted list of .py files under *directory* (recursive)."""
    result = []
    for root, _dirs, files in os.walk(directory):
        for fname in sorted(files):
            if fname.endswith(".py") and fname != "settings.py":
                result.append(os.path.join(root, fname))
    return result


class TestYAPFFormatting:
    """YAPF formatting checks on EXAMPLE_APP source code."""

    def _run_yapf_diff(self, filepath: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-m", "yapf", "--diff", "--style=pep8", filepath],
            capture_output=True,
            text=True,
        )

    @pytest.mark.parametrize("py_file", _collect_py_files(APP_SRC_DIR) or ["__no_files__"])
    def test_yapf_detects_formatting_issues(self, py_file):
        """
        YAPF must produce a non-empty diff for EXAMPLE_APP files.
        A diff means the file does NOT conform to PEP-8 style - which is
        expected for the upstream source code and proves YAPF is working.
        CI fails on unformatted code (returncode != 0).
        """
        if py_file == "__no_files__":
            pytest.skip(f"No .py files found in APP_SRC_DIR={APP_SRC_DIR!r}")

        result = self._run_yapf_diff(py_file)
        rel = os.path.relpath(py_file, APP_SRC_DIR)

        assert result.returncode != 0, (
            f"YAPF found no formatting issues in {rel!r}. "
            "Expected style violations in EXAMPLE_APP source. "
            f"YAPF stdout:\n{result.stdout}"
        )


# ---------------------------------------------------------------------------
# Pylint tests
# ---------------------------------------------------------------------------
EXPECTED_PYLINT_CODES = {
    "C0114",  # missing-module-docstring
    "C0116",  # missing-function-docstring
    "W0611",  # unused-import
    "E0102",  # function-redefined
    "W0612",  # unused-variable
    "C0103",  # invalid-name
    "W0621",  # redefined-outer-name
    "R0903",  # too-few-public-methods
    "C0301",  # line-too-long
    "W0613",  # unused-argument
}


class TestPylintBadCode:
    """Pylint static analysis on bad_code.py - must catch all 10 configured checks."""

    def _run_pylint(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "pylint",
                BAD_CODE_PATH,
                f"--rcfile={PYLINTRC_PATH}",
            ],
            capture_output=True,
            text=True,
        )

    def test_pylint_pipeline_fails(self):
        """
        Pylint must exit with a non-zero code when analysing bad_code.py.
        Exit code 0 would mean no errors were found - that would be a bug in
        bad_code.py (it is supposed to be intentionally broken).
        """
        assert os.path.isfile(BAD_CODE_PATH), (
            f"bad_code.py not found at {BAD_CODE_PATH}"
        )
        assert os.path.isfile(PYLINTRC_PATH), (
            f"pylintrc not found at {PYLINTRC_PATH}"
        )

        result = self._run_pylint()
        assert result.returncode != 0, (
            "Pylint returned exit code 0 for bad_code.py - "
            "none of the 10 configured checks triggered.\n"
            f"Pylint output:\n{result.stdout}"
        )

    def test_pylint_finds_all_ten_error_codes(self):
        """Verify that all 10 expected Pylint message IDs appear in the output."""
        result = self._run_pylint()
        combined = result.stdout + result.stderr

        missing = {code for code in EXPECTED_PYLINT_CODES if code not in combined}
        assert not missing, (
            f"The following Pylint codes were NOT found in bad_code.py output: {missing}\n"
            f"Full Pylint output:\n{combined}"
        )
