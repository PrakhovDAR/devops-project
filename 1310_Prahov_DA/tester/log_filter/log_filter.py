import sys
import logging

class LevelFilter(logging.Filter):
    def __init__(self, level):
        self.level = level
    def filter(self, record):
        return record.levelno == self.level

log_filter = logging.getLogger('tester')
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
log_filter.setLevel(logging.INFO) 

# Обработчик stdout
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.INFO)
stdout_handler.setFormatter(formatter)
stdout_handler.addFilter(LevelFilter(logging.INFO))

# Обработчик stderr
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.ERROR)
stderr_handler.setFormatter(formatter)
stderr_handler.addFilter(LevelFilter(logging.ERROR))

# Добавить обработчики
log_filter.addHandler(stdout_handler)
log_filter.addHandler(stderr_handler)