from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="code_review_assistant",
    version="0.1.0",
    author="LeoLLM",
    author_email="y.leo.scholar@gmail.com",
    description="Automated code review assistant with templates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LeoLLM/code-review-assistant-2",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "code-review-assistant=code_review_assistant.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "code_review_assistant": ["templates/*.md", "config/*.yaml"],
    },
)