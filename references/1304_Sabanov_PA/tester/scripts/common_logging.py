import sys
from datetime import datetime
from typing import TextIO


def _timestamp() -> str:
	return datetime.now().strftime(r'%Y-%m-%d %H:%M:%S')


def log(message: str, *, stream: TextIO = sys.stdout, stream_name: str = 'stdout') -> None:
	line = f'[{_timestamp()}] [{stream_name}] {message}\n'
	stream.write(line)
	stream.flush()
	try:
		with open('/proc/1/fd/1', 'a', encoding='utf-8') as docker_stdout:
			docker_stdout.write(line)
			docker_stdout.flush()
	except OSError:
		pass