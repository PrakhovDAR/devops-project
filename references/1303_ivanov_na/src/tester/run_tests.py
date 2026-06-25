import os
import subprocess
import sys
from pathlib import Path

ROOT = Path("/opt/project")
LOG_STDOUT = Path(os.getenv("LOG_STDOUT", "/opt/tester/logs/stdout.log"))
LOG_STDERR = Path(os.getenv("LOG_STDERR", "/opt/tester/logs/stderr.log"))

STAGES = {
    "html": ROOT / "tester" / "tests" / "test_html_lint.py",
    "pylint": ROOT / "tester" / "tests" / "test_pylint_static.py",
    "integration": ROOT / "tester" / "tests" / "test_upload_integration.py",
}


def write_log(path, line):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as log_file:
        log_file.write(line + "\n")


def out(line):
    print(line, flush=True)
    write_log(LOG_STDOUT, line)


def err(line):
    print(line, file=sys.stderr, flush=True)
    write_log(LOG_STDERR, line)


def run_stage(stage, test_file):
    command = [sys.executable, "-m", "pytest", "-q", str(test_file)]
    out(f"[{stage}] start: {' '.join(command)}")
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.stdout:
        for line in result.stdout.splitlines():
            out(f"[{stage}] {line}")
    if result.stderr:
        for line in result.stderr.splitlines():
            err(f"[{stage}] {line}")
    out(f"[{stage}] exit_code={result.returncode}")
    return result.returncode


def main():
    requested = [name.strip() for name in os.getenv("TEST_STAGES", "").split(",") if name.strip()]
    stages = requested or list(STAGES)
    failures = 0
    for stage in stages:
        test_file = STAGES.get(stage)
        if test_file is None:
            err(f"[runner] unknown stage: {stage}")
            failures += 1
            continue
        failures += 1 if run_stage(stage, test_file) != 0 else 0
    out(f"[runner] failures={failures}")
    return failures


if __name__ == "__main__":
    sys.exit(main())
