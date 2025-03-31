#!/usr/bin/env python3
"""
Notion 项目更新器 - 安装脚本
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="notion-project-updater",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="自动扫描代码项目并同步到 Notion 数据库的工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/notion-project-updater",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "notion-updater=main:main",
        ],
    },
)
