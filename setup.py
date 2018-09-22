from setuptools import setup

long_description = """
What is detox?
==========================

detox is the distributed version of "tox".  It makes efficient use of multiple
CPUs by running all possible activities in parallel.  It has the same options
and configuration that tox has so after installation can just run::

    detox

in the same way and with the same options with which you would run
``tox``, see the `tox home page`_ for more info.

Please file issues as "tox" issues using the "detox" label:

    https://github.com/tox-dev/tox/issues

.. note::

    detox runs on python2.7 and python3.4+ (but supports creation of
    all environments supported of the underlying "tox" command)

.. _`tox home page`: http://tox.readthedocs.org
"""


def main():
    setup(
        name='detox',
        description='distributing activities of the tox tool',
        long_description=long_description,
        version='0.14.post1',  # Note: keep in sync with detox/__init__.py
        url='https://github.com/tox-dev/detox',
        license='MIT',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='holger krekel',
        author_email='holger@merlinux.eu',
        classifiers=['Development Status :: 4 - Beta',
                     'Framework :: tox',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Topic :: Software Development :: Testing',
                     'Topic :: Software Development :: Libraries',
                     'Topic :: Utilities',
                     'Programming Language :: Python',
                     ],
        packages=['detox'],
        install_requires=['tox>=2,<4', 'py>=1.4.27', 'eventlet>=0.15.0'],
        entry_points={'console_scripts': 'detox=detox.main:main',
                      'tox': ['proclimit = detox.tox_proclimit']},
    )


if __name__ == '__main__':
    main()
