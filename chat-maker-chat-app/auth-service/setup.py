from setuptools import find_packages, setup

setup(
    name="chat-maker-auth-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.78.0",
        "uvicorn[standard]",
        "arrow==1.2.3",
        "PyJWT==2.5.0",
        "pycryptodome==3.16.0",
        "python-multipart==0.0.5",
    ],
)
