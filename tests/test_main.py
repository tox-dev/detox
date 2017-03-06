# -*- coding: utf-8 -*-


import subprocess
import sys


def invoke(command, success_codes=(0,)):
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        status = 0
    except subprocess.CalledProcessError as error:
        output = error.output
        status = error.returncode
    output = output.decode('utf-8')
    if status not in success_codes:
        raise Exception(
            'Command %r return exit code %d and output: """%s""".' % (
                command,
                status,
                output,
            )
        )
    return status, output


def test_run_as_module():
    """Can be run as `python -m detox ...`."""
    status, output = invoke([
        sys.executable, '-m', 'detox', '--help',
    ])
    assert status == 0
    assert output.startswith('usage:')
