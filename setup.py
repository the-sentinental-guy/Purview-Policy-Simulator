from setuptools import setup, find_packages

setup(
    name="purview-policy-simulator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.23.0",
        "scikit-learn>=1.3.0",
        "pydantic>=2.0.0",
        "httpx>=0.24.0",
        "python-multipart>=0.0.6",
        "jinja2>=3.1.0",
        "numpy>=1.24.0",
    ],
    python_requires=">=3.9",
    description="Microsoft Purview Policy Simulator using NLP and TF-IDF matching",
    author="Purview Policy Simulator",
)
