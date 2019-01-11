import io
from setuptools import setup


def make_long_description():
    with io.open("README.md", encoding='UTF-8') as f:
        readme = f.read()
    with io.open("CHANGELOG", encoding='UTF-8') as f:
        changelog = f.read()
    return readme + "\n\n" + changelog


setup(
    name="detox",
    description="distributing activities of the tox tool",
    long_description=make_long_description(),
    long_description_content_type="text/markdown",
    version="0.19",  # Note: keep in sync with detox/__init__.py
    url="https://github.com/tox-dev/detox",
    license="MIT",
    platforms=["unix", "linux", "osx", "cygwin", "win32"],
    author="holger krekel",
    author_email="holger@merlinux.eu",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: tox",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Programming Language :: Python",
    ],
    packages=["detox"],
    install_requires=["tox>=3.5,<3.7", "py>=1.4.27", "eventlet>=0.15.0"],
    extras_require={"lint": ["black", "flake8"], "dev": ["pytest >= 3.8"]},
    entry_points={
        "console_scripts": "detox=detox.cli:main",
        "tox": ["proclimit = detox.tox_proclimit"],
    },
)
