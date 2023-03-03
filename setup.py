from setuptools import setup, find_packages

setup(
    name="flask-server",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask",
        "requests",
        "pymysql"
    ],
    entry_points={
        "console_scripts": [
            "flask-server=server:app"
        ]
    },
    author="olebbj",
    author_email="olebbj@gmail.com",
    description="A Flask server with API endpoints",
    url="http://127.0.0.1:5001",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
