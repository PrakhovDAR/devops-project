import subprocess
from log_filter import log_filter

class StaticAnalys:
    def __init__(self):
        self.path_app = "../app"
        self.criteria = (
            "syntax-error,"
            "undefined-variable,"
            "unused-import,"
            "unused-variable,"
            "redefined-builtin,"
            "bad-indentation,"
            "missing-final-newline,"
            "trailing-whitespace,"
            "unreachable,"
            "duplicate-key"
        )
        log_filter.info("Starting static analysis by 10 criteria")

    def run_test(self):
        result = subprocess.run([
            "pylint",
            "--disable=all",
            f"--enable={self.criteria}",
            self.path_app
        ], capture_output=True, text=True)
        
        if result.stdout:
            log_filter.info(result.stdout)
        if result.stderr:
            log_filter.error(result.stderr)
        log_filter.info(f"Static analysis finished (Return code: {result.returncode})")