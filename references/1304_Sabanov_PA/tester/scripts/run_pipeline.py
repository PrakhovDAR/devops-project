import os
import subprocess
import sys

from common_logging import log

STAGES_ENV = os.getenv('TEST_STAGES', 'yapf,pylint,headers')
SELECTED_STAGES = [s.strip() for s in STAGES_ENV.split(',') if s.strip()]

STAGE_SCRIPTS = {
	'yapf': ['python3', '/opt/project/scripts/test_yapf.py'],
	'pylint': ['python3', '/opt/project/scripts/test_pylint.py'],
	'headers': ['python3', '/opt/project/scripts/test_headers.py'],
}


def run_stage(name: str, command: list[str]) -> int:
	log(f'===== Starting stage: {name} =====')
	proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
	assert proc.stdout and proc.stderr

	for line in proc.stdout:
		print(line.rstrip('\n'))
	for line in proc.stderr:
		print(line.rstrip('\n'))

	returncode = proc.wait()
	if returncode != 0:
		log(f'===== Stage {name} FAILED (exit {returncode}) =====',
			stream_name='stderr')
	else:
		log(f'===== Stage {name} PASSED =====')
	return returncode


def main() -> int:
	log(f'Starting test pipeline. Selected stages: {", ".join(SELECTED_STAGES)}')
	failed = False
	for stage in SELECTED_STAGES:
		if stage not in STAGE_SCRIPTS:
			log(f'Unknown stage "{stage}" - skipping', stream_name='stderr')
			continue
		code = run_stage(stage, STAGE_SCRIPTS[stage])
		if code != 0:
			failed = True
	if failed:
		log('Some test stages failed', stream_name='stderr')
		return 1
	log('All selected test stages completed successfully')
	return 0


if __name__ == '__main__':
	raise SystemExit(main())