import subprocess
import sys
import unittest

from common_logging import log

TARGETS = [
	'/opt/project/EXAMPLE_APP',
]


class TestYapf(unittest.TestCase):
	def test_yapf(self):
		log('Starting YAPF formatting check')
		command = ['python3', '-m', 'yapf', '--diff', '--recursive', *TARGETS]
		proc = subprocess.run(command, capture_output=True, text=True, check=False)

		if proc.stdout.strip():
			log('YAPF found formatting issues:', stream=sys.stderr, stream_name='stderr')
			for line in proc.stdout.splitlines():
				log(line, stream=sys.stderr, stream_name='stderr')
			log('YAPF formatting issues found', stream_name='stderr')
			self.fail('YAPF formatting issues found')

		if proc.stderr.strip():
			for line in proc.stderr.splitlines():
				log(line, stream=sys.stderr, stream_name='stderr')

		log('YAPF formatting check passed')


if __name__ == '__main__':
	unittest.main()