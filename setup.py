"""
(C) 1995-2023 Epicor Software Corporation. All Rights Reserved.

The copyright owner has not given any authority for any publication
of this work.  This work contains valuable trade secrets of Epicor
and must be maintained in confidence.  Use of this work is governed
by the terms and conditions of a license agreement with Epicor.

"""

import os

from os import path
from setuptools import (
    find_packages,
    setup)


here = path.abspath(path.dirname(__file__))


# -----------------------------------------------------------------------------
# --- Get the long Description from the `README` File.
# -----------------------------------------------------------------------------
with open(path.join(here, "README.md"), "r") as f:
    """Docstring."""
    long_description = f.read()


def package_files(directory, home_dir):
    """Docstring."""
    paths = []

    # -------------------------------------------------------------------------
    # --- Iterate over the Directory, passed here.
    for (p, directories, filenames) in os.walk(directory):
        files = []

        for filename in filenames:
            files.append(os.path.join(p, filename))

        paths.append((os.path.join(home_dir, "src", *p.split(os.sep)[1:]), files))

    return paths


setup(
    name="EPA State Machine",
    version="0.0.0",
    description="",
    long_description=long_description,
    url="https://gitlab.toogoerp.net/pbotelho/epa_state_machine",
    author="",
    author_email="",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 5 - Production/Stable",
        "Environment :: UNIX System V",
        "Framework :: Sphinx",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Go",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.9.6",
        "Topic :: Database",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Games/Entertainment",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    install_requires=[
        "Django==4.1.5",
        "aioredis==2.0.1",
        "channels==4.0.0",
        "channels-redis==4.0.0",
        "coverage==7.2.7",
        "django-redis==5.2.0",
        "gunicorn==20.1.0",
        "httpx==0.24.0",
        "ipython==8.13.2",
        "jwt==1.3.1",
        "markdown==3.4.3",
        "mock==5.1.0",
        "pep8==1.7.1",
        "pep257==0.7.0",
        "psycopg2-binary==2.9.5",
        "pycodestyle==2.5.0",
        "pylint==2.15.10",
        "pylint-django==2.5.3",
        "pytest==7.4.0",
        "python-decouple==3.8",
        "rel==0.4.8",
        "requests==2.28.2",
        "uvicorn[standard]",
        "websocket-client==1.5.1",
    ],
    license="",
)
