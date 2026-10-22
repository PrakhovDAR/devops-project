import subprocess
from log_filter import log_filter

class CodeStyle:
    def __init__(self):
        self.path_app = "../app"
        log_filter.info("Running check code style with yapf")
    
    def run_test(self):
        result = subprocess.run(
            ["yapf", "--diff", "--recursive", self.path_app],
            capture_output=True,
            text=True
        )
        if result.stdout:
            log_filter.info(result.stdout)
        if result.stderr:
            log_filter.error(result.stderr)
        log_filter.info(f"Code style check with yapf finished (Return code: {result.returncode})")