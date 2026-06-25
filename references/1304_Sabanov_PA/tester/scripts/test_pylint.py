import subprocess
import unittest
from pathlib import Path

from common_logging import log

APP_SOURCE = Path('/opt/project/EXAMPLE_APP')

PYLINT_CHECKS = [
	'invalid-name',
	'missing-module-docstring',
	'missing-function-docstring',
	'multiple-imports',
	'wrong-import-order',
	'pointless-string-statement',
	'unused-import',
	'unused-variable',
	'redefined-builtin',
	'broad-except',
]


class TestPylint(unittest.TestCase):
	def test_pylint(self):
		log('Starting Pylint static analysis with 10 criteria')
		python_files = sorted(APP_SOURCE.glob('*.py'))
		if not python_files:
			self.fail('No Python files found')

		command = [
			'pylint',
			'--disable=all',
			f'--enable={",".join(PYLINT_CHECKS)}',
			'--exit-zero',
		] + [str(f) for f in python_files]

		proc = subprocess.run(command, capture_output=True, text=True, check=False)

		if proc.stdout:
			for line in proc.stdout.splitlines():
				log(line)
		if proc.stderr:
			for line in proc.stderr.splitlines():
				log(line, stream_name='stderr')

		if proc.returncode == 0:
			log(f'Pylint finished with exit code {proc.returncode}')
		else:
			log(f'Pylint finished with exit code {proc.returncode}', stream_name='stderr')
			self.fail(f'Pylint finished with exit code {proc.returncode}')


if __name__ == '__main__':
	unittest.main()