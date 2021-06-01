from setuptools import setup, find_packages

import vis4wave

base_packages = [
    "pyvis>=0.1.9",
    "h2o_wave>=0.16.0",
]

docs_packages = [
    "mkdocs==1.1",
    "mkdocs-material==4.6.3",
    "mkdocstrings==0.8.0",
]

test_packages = [
    "flake8>=3.6.0",
    "nbval>=0.9.1",
    "pytest>=4.0.2",
    "pytest-xdist>=1.32.0",
    "black>=19.3b0",
    "pytest-cov>=2.6.1",
    "pytest-mock>=1.6.3",
    "pre-commit>=1.18.3",
    "nbval>=0.9.6",
    # "matplotlib>=3.0.2",
    "mktestdocs==0.1.1",
]

util_packages = [
    "jupyter>=1.0.0",
]

dev_packages = docs_packages + test_packages + util_packages


setup(
    name="pyvis4wave",
    version=vis4wave.__version__,
    description="Bring interactive network visualization to H2O wave web-apps",
    author="Jean-Matthieu Schertzer",
    packages=find_packages(exclude=["notebooks"]),
    # package_data={
    #     "vis4wave": [
    #         "data/*.zip",
    #         "images/*.png",
    #         "static/*/*.css",
    #         "static/*/*.js",
    #         "static/*/*.html",
    #     ]
    # },
    install_requires=base_packages,
    extras_require={"docs": docs_packages, "dev": dev_packages, "test": test_packages},
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: Apache License",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
