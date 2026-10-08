"""
Master test pipeline runner.

Stages:
  1. YAPF   - formatting check on EXAMPLE_APP source (expected: FAIL, issues found)
  2. Pylint - static analysis of bad_code.py (expected: FAIL, 10 errors found)
  3. Integration - HTTP tests against the live app (expected: PASS)

Each log line is prefixed with a timestamp.
Exit code:
  0 - all stages produced the expected result
  1 - at least one stage produced an unexpected result
"""
import os
import subprocess
import sys
from datetime import datetime


def log(message: str) -> None:
    """Print *message* to stdout with a leading ISO-8601 timestamp."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {message}", flush=True)


def _run_pytest(test_path: str, extra_flags: list = None) -> int:
    """Run pytest on *test_path*, stream output line-by-line, return exit code."""
    cmd = [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short", "--no-header"]
    if extra_flags:
        cmd.extend(extra_flags)

    log(f"CMD: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in proc.stdout:
        log(line.rstrip())
    proc.wait()
    return proc.returncode


def stage_static() -> int:
    """Run YAPF + Pylint tests via pytest."""
    log("=" * 60)
    log("STAGE 1: Static analysis  (YAPF + Pylint)")
    log("=" * 60)
    return _run_pytest("/tester/tests/test_pylint_static.py")


def stage_integration() -> int:
    """Run HTTP integration tests via pytest."""
    log("=" * 60)
    log("STAGE 2: Integration tests  (requests)")
    log("=" * 60)
    return _run_pytest("/tester/tests/test_integration.py")


def main() -> None:
    log("#" * 60)
    log("Starting full test pipeline")
    log("#" * 60)

    results = {
        "Static (YAPF+Pylint)": stage_static(),
        "Integration":          stage_integration(),
    }

    log("=" * 60)
    log("PIPELINE SUMMARY")
    log("=" * 60)
    overall_ok = True
    for stage_name, code in results.items():
        status = "PASS" if code == 0 else "FAIL"
        log(f"  {stage_name:<25s} exit={code}  [{status}]")
        if code != 0:
            overall_ok = False

    if overall_ok:
        log("OVERALL: ALL STAGES PASSED")
        sys.exit(0)
    else:
        log("OVERALL: SOME STAGES FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
