[![Build Status](https://travis-ci.org/tox-dev/detox.svg?branch=master)](https://travis-ci.org/tox-dev/detox)
[![Latest Version on PyPI](https://badge.fury.io/py/detox.svg)](https://badge.fury.io/py/detox)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/detox.svg)](https://pypi.org/project/detox/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# What is detox?

detox is the distributed version of [tox](https://pypi.org/project/tox/).  It makes efficient use of multiple CPUs by running all possible activities in parallel.  It has the same options and configuration that tox has so after installation can just run:

    detox

in the same way and with the same options with which you would run `tox`, see the [tox home page](http://tox.readthedocs.io) for more info.

Additionally, detox offers a `-n` or `--num` option to set the number of concurrent processes to use.

**NOTE** due to the concurrent execution of the testenvs the output of the different testruns is not printed to the terminal. Instead they are logged into separate files inside the `log` directories of the testenvs.
