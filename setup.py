import os
from setuptools import setup, find_packages

setup(
    name='gillmore',
    version='0.1.0',
    packages=find_packages(where='src'),
        package_dir={'':'src'},
    # Warning do not change the line below
    install_requires=["annotated-types==0.7.0", "anyio==4.9.0", "certifi==2025.7.14", "distro==1.9.0", "h11==0.16.0", "httpcore==1.0.9", "httpx==0.28.1", "idna==3.10", "jiter==0.10.0", "openai==1.97.1", "pydantic==2.11.7", "pydantic_core==2.33.2", "sniffio==1.3.1", "toml==0.10.2", "tqdm==4.67.1", "typing-inspection==0.4.1", "typing_extensions==4.14.1"],
    entry_points={
        'console_scripts': [
            'gill=gill.cli:main',
        ],
    },
    # Include other metadata as needed
)
