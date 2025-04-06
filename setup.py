from setuptools import setup, find_packages

setup(
    name="featureflux",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "redis",
        "kafka-python",
        "click",
        "pyyaml",
        "pydantic",
        "pandas",
        "pyspark",
        "transformers",
        "torch",
        "torchvision",
        "scikit-learn",
        "joblib",
        "tensorflow",
    ],
    entry_points={
        'console_scripts': [
            'featureflux=src/service/cli:main'
        ]
    },
)