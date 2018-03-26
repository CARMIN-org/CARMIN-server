"""
CARMIN Setup
"""
from setuptools import setup, find_packages

NAME = "carmin-server"
VERSION = "0.5.4"
DEPS = [
    "flask-restful", "flask-sqlalchemy", "psycopg2-binary", "marshmallow",
    "marshmallow_enum==1.4.*", "boutiques", "blinker"
]

setup(
    name=NAME,
    version=VERSION,
    description=
    "REST API for exchanging data and remotely calling pipelines on CBrain",
    url="https://github.com/fli-iam/CARMIN",
    author="CARMIN",
    author_email="carmin@googlegroups.com",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent"
    ],
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    test_suite="pytest",
    tests_require=["pytest"],
    setup_requires=DEPS,
    install_requires=DEPS,
    entry_points={"console_scripts": ["server=server.__main__:main"]},
    data_files=[],
    zip_safe=False)
