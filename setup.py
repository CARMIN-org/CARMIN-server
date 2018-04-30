from setuptools import setup, find_packages

NAME = "carmin-server"
VERSION = "0.1"
DEPS = [
    "flask-restful>=0.3.6,<1.0", "flask-sqlalchemy>-2.3.2,<3.0",
    "psycopg2-binary>=2.7.4,<3.0", "marshmallow>=2.15.0,<3.0",
    "marshmallow_enum>=1.4.1,<2.0", "boutiques>=0.5.6,<1.0",
    "blinker>=1.4,<2.0", "typing>=3.6.4,<4.0", "scandir>=1.7,<2.0",
    "psutil>=5.4.5,<6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Server for exchanging data and remotely calling pipelines",
    url="https://github.com/CARMIN-org/CARMIN-server",
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
