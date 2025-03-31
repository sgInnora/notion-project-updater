#!/usr/bin/env python3
"""
Notion 项目更新器 - 测试运行器
"""

import unittest
import os
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

def run_tests():
    """运行所有测试"""
    console = Console()
    
    console.print(Panel.fit(
        "[bold cyan]Notion 项目更新器 - 测试运行器[/bold cyan]",
        title="开始测试"
    ))
    
    # 获取测试目录
    test_dir = Path(__file__).parent / "tests"
    
    # 添加项目根目录到导入路径
    sys.path.insert(0, str(Path(__file__).parent))
    
    # 发现并运行所有测试
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(test_dir), pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 打印测试结果摘要
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    passed = tests_run - failures - errors - skipped
    
    console.print(Panel.fit(
        f"[bold]测试摘要[/bold]\n"
        f"运行: {tests_run}\n"
        f"通过: [green]{passed}[/green]\n"
        f"失败: [red]{failures}[/red]\n"
        f"错误: [red]{errors}[/red]\n"
        f"跳过: [yellow]{skipped}[/yellow]",
        title="测试完成"
    ))
    
    return failures == 0 and errors == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
