# What is detox?

detox is the distributed version of [tox](https://pypi.org/project/tox/).  It makes efficient use of multiple CPUs by running all possible activities in parallel.  It has the same options and configuration that tox has so after installation can just run:

    detox

in the same way and with the same options with which you would run `tox`, see the [tox home page](http://tox.readthedocs.io) for more info.

Please file issues as ["tox" issues](https://github.com/tox-dev/tox/issues) using a "detox: " prefix in the issue title.

## Note

detox runs only on python2.6 and python2.7 (but supports creation of python3 and all environments supported of the underlying "tox" command)
