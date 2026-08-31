from setuptools import setup, find_packages

setup(
    name="timekeeper-daily",
    version="0.1.0",
    packages=find_packages(include=["core", "tasks"]),
    python_requires=">=3.10",
    install_requires=[
        "pywin32",
        "mss",
        "opencv-python",
        "numpy",
        "pydirectinput",
        "PyYAML",
    ],
)
