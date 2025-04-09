from setuptools import setup, find_packages

setup(
    name="featureflux",
    version="0.1.0",
    description="A modular, scalable ML serving platform integrating deep learning, statistical analysis, and distributed systems.",
    author="Vishal Srivastava",
    author_email="srivasv3@uci.edu",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.95.2",
        "uvicorn==0.22.0",
        "kafka-python==2.0.2",
        "redis==4.5.5",
        "pandas==1.5.3",
        "scikit-learn==1.2.2",
        "numpy==1.23.5",
        "pyspark==3.3.1",
        "pgmpy==0.1.18",
        "click==8.1.3",
        "python-dotenv==0.21.0",
        "torch==2.0.1",
        "torchvision==0.15.2",
        "tensorflow-macos==2.12.0",
        "tensorflow-metal==0.6.0"
    ],
    entry_points={
        'console_scripts': [
            'featureflux=service.cli:main',  # This exposes the CLI tool as "featureflux"
        ]
    },
)