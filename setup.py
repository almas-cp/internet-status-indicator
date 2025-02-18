from setuptools import setup, find_packages

setup(
    name="network-status-indicator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "PyQt5>=5.15.0",
    ],
    entry_points={
        'console_scripts': [
            'network-status-indicator=network_status_indicator:main',
        ],
    },
    author="almas-cp",
    description="A cross-platform network connectivity status indicator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/almas-cp/internet-status-indicator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)