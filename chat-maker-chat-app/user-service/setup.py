from setuptools import find_packages, setup

setup(
    name="chat-maker-user-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.78.0",
        "uvicorn[standard]",
    ],
)
