import os, sys

from setuptools import setup

long_description="""
What is detox?
==========================

detox is the distributed version of "tox".  It makes efficient use of multiple
CPUs by running all possible activities in parallel.  It has the same options
and configuration that tox has so after installation can just run::

    detox

in the same way and with the same options with which you would run
``tox``, see the `tox home page`_ for more info.

Please file issues as "tox" issues using the "detox" component:

    https://bitbucket.org/hpk42/tox/issues

.. note::

    detox runs only on python2.6 and python2.7 (but supports creation of
    python3 and all environments supported of the underlying "tox" command)

.. _`tox home page`: http://tox.testrun.org/
"""

def main():
    setup(
        name='detox',
        description='distributing activities of the tox tool (py2 only)',
        long_description = long_description,
        version='0.9.4',
        url='http://bitbucket.org/hpk42/detox',
        license='MIT',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='holger krekel',
        author_email='holger at merlinux.eu',
        classifiers=['Development Status :: 4 - Beta',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Software Development :: Testing',
                     'Topic :: Software Development :: Libraries',
                     'Topic :: Utilities',
                     'Programming Language :: Python',
                     ],
        packages=['detox', ],
        install_requires=['tox>=1.9.0',
            'py>=1.4.13', 'eventlet>=0.15.0',],
        entry_points={'console_scripts': 'detox=detox.main:main'},
    )

if __name__ == '__main__':
    main()
