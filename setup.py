from setuptools import setup


def main():
    setup(
        name='detox',
        description='distributing activities of the tox tool',
        long_description=open("README.md").read(),
        long_description_content_type='text/markdown',
        version='0.14.post3',  # Note: keep in sync with detox/__init__.py
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
