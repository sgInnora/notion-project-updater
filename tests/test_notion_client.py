#!/usr/bin/env python3
"""
Notion 项目更新器 - Notion 客户端测试
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# 添加父目录到导入路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notion_client import NotionClient

class TestNotionClient(unittest.TestCase):
    """Notion 客户端测试类"""
    
    def setUp(self):
        """设置测试环境"""
        self.api_key = "test_api_key"
        self.database_id = "test_database_id"
        self.client = NotionClient(self.api_key, self.database_id)
    
    @patch('requests.post')
    def test_load_existing_projects(self, mock_post):
        """测试加载已存在项目"""
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [
                {
                    "id": "page1",
                    "properties": {
                        "名称": {
                            "title": [
                                {
                                    "text": {
                                        "content": "项目1"
                                    }
                                }
                            ]
                        }
                    }
                },
                {
                    "id": "page2",
                    "properties": {
                        "名称": {
                            "title": [
                                {
                                    "text": {
                                        "content": "项目2"
                                    }
                                }
                            ]
                        }
                    }
                }
            ]
        }
        
        mock_post.return_value = mock_response
        
        # 调用被测函数
        projects = self.client.load_existing_projects()
        
        # 验证结果
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects["项目1"], "page1")
        self.assertEqual(projects["项目2"], "page2")
        
        # 验证 API 调用
        mock_post.assert_called_once()
    
    @patch('requests.post')
    def test_create_project(self, mock_post):
        """测试创建项目"""
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "new_page_id"
        }
        
        mock_post.return_value = mock_response
        
        # 测试数据
        project_info = {
            "name": "测试项目",
            "path": "/path/to/project",
            "tech_stack": ["Python", "React"],
            "project_type": "Web应用",
            "status": "活跃",
            "priority": "高",
            "description": "这是一个测试项目",
            "last_modified": "2025-03-31"
        }
        
        # 调用被测函数
        page_id = self.client.create_project(project_info)
        
        # 验证结果
        self.assertEqual(page_id, "new_page_id")
        
        # 验证 API 调用
        mock_post.assert_called_once()
    
    @patch('requests.patch')
    def test_update_project(self, mock_patch):
        """测试更新项目"""
        # 模拟 API 响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": "page_id"
        }
        
        mock_patch.return_value = mock_response
        
        # 测试数据
        project_info = {
            "name": "测试项目",
            "path": "/path/to/project",
            "tech_stack": ["Python", "React"],
            "project_type": "Web应用",
            "status": "活跃",
            "priority": "高",
            "description": "这是一个更新后的测试项目",
            "last_modified": "2025-03-31"
        }
        
        # 调用被测函数
        result = self.client.update_project("page_id", project_info)
        
        # 验证结果
        self.assertTrue(result)
        
        # 验证 API 调用
        mock_patch.assert_called_once()
    
    def test_build_properties(self):
        """测试构建 Notion 属性"""
        # 测试数据
        project_info = {
            "name": "测试项目",
            "path": "/path/to/project",
            "tech_stack": ["Python", "React"],
            "project_type": "Web应用",
            "status": "活跃",
            "priority": "高",
            "description": "这是一个测试项目",
            "last_modified": "2025-03-31"
        }
        
        # 调用被测函数
        properties = self.client._build_properties(project_info)
        
        # 验证结果
        self.assertEqual(properties["名称"]["title"][0]["text"]["content"], "测试项目")
        self.assertEqual(properties["路径"]["rich_text"][0]["text"]["content"], "/path/to/project")
        self.assertEqual(len(properties["技术栈"]["multi_select"]), 2)
        self.assertEqual(properties["项目类型"]["select"]["name"], "Web应用")
        self.assertEqual(properties["状态"]["select"]["name"], "活跃")
        self.assertEqual(properties["优先级"]["select"]["name"], "高")
        self.assertEqual(properties["描述"]["rich_text"][0]["text"]["content"], "这是一个测试项目")
        self.assertEqual(properties["最后修改日期"]["date"]["start"], "2025-03-31")

if __name__ == "__main__":
    unittest.main()
