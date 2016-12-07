# What is detox?

detox is the distributed version of "tox".  It makes efficient use of multiple
CPUs by running all possible activities in parallel.  It has the same options
and configuration that tox has so after installation can just run::

    detox

in the same way and with the same options with which you would run
``tox``, see the `tox home page`_ for more info.

Please file issues as "tox" issues using the "detox" label:

    https://github.com/tox-dev/tox/issues

.. note::

    detox runs only on python2.6 and python2.7 (but supports creation of
    python3 and all environments supported of the underlying "tox" command)

.. _`tox home page`: http://tox.readthedocs.org
