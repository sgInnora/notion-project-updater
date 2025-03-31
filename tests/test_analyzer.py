#!/usr/bin/env python3
"""
Notion 项目更新器 - 项目分析器测试
"""

import os
import sys
import unittest
from pathlib import Path

# 添加父目录到导入路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from analyzer import (
    detect_tech_stack,
    detect_project_type,
    detect_project_status,
    detect_project_priority,
    extract_description,
    get_last_modified_date
)

class TestAnalyzer(unittest.TestCase):
    """项目分析器测试类"""
    
    def setUp(self):
        """设置测试环境"""
        # 使用测试目录作为测试项目
        self.test_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        
        # 创建一个示例测试项目目录
        self.test_project_dir = self.test_dir / "test_project"
        self.test_project_dir.mkdir(exist_ok=True)
        
        # 创建一些测试文件
        (self.test_project_dir / "main.py").touch()
        (self.test_project_dir / "requirements.txt").touch()
        (self.test_project_dir / "README.md").write_text("# Test Project\n\nThis is a test project for testing the analyzer.")
    
    def tearDown(self):
        """清理测试环境"""
        # 清理测试文件
        for file in self.test_project_dir.glob("*"):
            file.unlink()
        
        # 删除测试项目目录
        self.test_project_dir.rmdir()
    
    def test_detect_tech_stack(self):
        """测试技术栈检测"""
        tech_stack = detect_tech_stack(self.test_project_dir)
        self.assertIsInstance(tech_stack, list)
        self.assertIn("Python", tech_stack)
    
    def test_detect_project_type(self):
        """测试项目类型检测"""
        tech_stack = ["Python"]
        project_type = detect_project_type(self.test_project_dir, tech_stack)
        self.assertIsInstance(project_type, str)
    
    def test_detect_project_status(self):
        """测试项目状态检测"""
        status = detect_project_status(self.test_project_dir)
        self.assertIn(status, ["活跃", "维护中", "暂停"])
    
    def test_detect_project_priority(self):
        """测试项目优先级检测"""
        priority = detect_project_priority(self.test_project_dir, "活跃")
        self.assertIn(priority, ["高", "中", "低"])
    
    def test_extract_description(self):
        """测试描述提取"""
        description = extract_description(self.test_project_dir)
        self.assertIsInstance(description, str)
        self.assertTrue(len(description) > 0)
    
    def test_get_last_modified_date(self):
        """测试最后修改日期获取"""
        date = get_last_modified_date(self.test_project_dir)
        self.assertIsInstance(date, str)
        self.assertTrue(len(date) > 0)

if __name__ == "__main__":
    unittest.main()
