# config.py
"""
全局配置文件，包含 Notion API 密钥、数据库 ID 和扫描目录等配置信息
"""

import os
from pathlib import Path

# Notion API 配置
NOTION_API_KEY = os.environ.get("NOTION_API_KEY", "your-secret-api-key") 
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID", "your-database-id")

# 扫描配置
SCAN_DIR = Path("/Users/anwu/Documents/code")

# 日志配置
LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / "app.log"

# 确保日志目录存在
LOG_DIR.mkdir(exist_ok=True)

# 技术栈检测配置
TECH_STACK_MARKERS = {
    "Python": [".py", "requirements.txt", "setup.py", "Pipfile", "poetry.lock", "pyproject.toml"],
    "JavaScript": [".js", "package.json", ".jsx", ".ts", ".tsx"],
    "React": ["react", ".jsx", ".tsx"],
    "Vue": ["vue", ".vue"],
    "Node.js": ["package.json", "node_modules"],
    "Go": [".go", "go.mod", "go.sum"],
    "Rust": [".rs", "Cargo.toml"],
    "Java": [".java", "pom.xml", "build.gradle"],
    "C/C++": [".c", ".cpp", ".h", ".hpp", "CMakeLists.txt", "Makefile"],
    "PHP": [".php", "composer.json"],
    "Ruby": [".rb", "Gemfile"],
    "Swift": [".swift", "Package.swift"],
    "Kotlin": [".kt", "build.gradle.kts"],
    "TypeScript": [".ts", ".tsx", "tsconfig.json"],
    "Flutter/Dart": [".dart", "pubspec.yaml"],
    "R": [".r", ".rmd", "DESCRIPTION"],
    "Shell": [".sh", ".bash", ".zsh"],
    "C#": [".cs", ".csproj", ".sln"],
    "HTML/CSS": [".html", ".htm", ".css"],
    "Jupyter": [".ipynb"],
}

# 项目类型检测配置
PROJECT_TYPE_MARKERS = {
    "Web应用": ["index.html", "public", "static", "react", "vue", "angular", "express", "flask", "django"],
    "CLI工具": ["cli", "command", "bin", "executable"],
    "服务端": ["server", "api", "backend", "service", "microservice", "fastapi", "express", "koa"],
    "移动应用": ["android", "ios", "flutter", "react-native", "mobile"],
    "库/框架": ["lib", "sdk", "framework", "package"],
    "机器学习": ["model", "train", "neural", "tensorflow", "pytorch", "keras", "scikit", "ml"],
    "数据分析": ["analysis", "data", "analytics", "visualization", "pandas", "numpy", "jupyter"],
    "游戏": ["game", "unity", "godot", "unreal"],
    "自动化脚本": ["script", "automation", "crawler", "scraper", "bot"],
    "区块链": ["blockchain", "web3", "eth", "smart contract", "solidity"],
}

# Git 相关配置
GIT_ACTIVE_THRESHOLD_DAYS = 30  # 30天内有提交视为活跃项目
GIT_MAINTENANCE_THRESHOLD_DAYS = 180  # 180天内有提交视为维护中项目
# 超过180天没有提交视为暂停项目

# 默认优先级策略（基于最后修改时间）
PRIORITY_THRESHOLDS = {
    "高": 30,   # 30天内修改过为高优先级
    "中": 90,   # 90天内修改过为中优先级
    "低": float('inf')  # 其他为低优先级
}
