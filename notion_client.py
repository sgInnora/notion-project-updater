# notion_client.py
"""
Notion API 交互模块，用于将项目信息同步到 Notion 数据库
"""

import time
import json
from typing import Dict, List, Any, Optional
import requests
from loguru import logger

from config import NOTION_API_KEY, NOTION_DATABASE_ID


class NotionClient:
    """Notion API 客户端"""
    
    def __init__(self, api_key: str, database_id: str):
        """初始化 Notion 客户端

        Args:
            api_key: Notion API 密钥
            database_id: Notion 数据库 ID
        """
        self.api_key = api_key
        self.database_id = database_id
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        # 验证配置
        if self.api_key == "your-secret-api-key" or self.database_id == "your-database-id":
            logger.warning("使用了默认的 API 密钥或数据库 ID，请更新 config.py 文件或设置环境变量")
    
    def load_existing_projects(self) -> Dict[str, str]:
        """从 Notion 数据库加载已存在项目

        Returns:
            项目名称到页面 ID 的映射
        """
        logger.info("从 Notion 加载已存在项目...")
        
        try:
            url = f"{self.base_url}/databases/{self.database_id}/query"
            response = requests.post(url, headers=self.headers, json={})
            
            if response.status_code != 200:
                logger.error(f"加载项目失败: {response.status_code} - {response.text}")
                return {}
            
            data = response.json()
            
            # 解析响应，提取项目名称和页面 ID
            projects = {}
            for page in data.get("results", []):
                properties = page.get("properties", {})
                title_property = properties.get("名称", {}).get("title", [])
                
                if title_property:
                    project_name = title_property[0].get("text", {}).get("content", "")
                    project_id = page.get("id", "")
                    
                    if project_name and project_id:
                        projects[project_name] = project_id
            
            logger.info(f"已加载 {len(projects)} 个已存在项目")
            return projects
            
        except Exception as e:
            logger.error(f"加载项目时出错: {str(e)}")
            return {}
    
    def create_project(self, project_info: Dict[str, Any]) -> Optional[str]:
        """在 Notion 中创建新项目页面

        Args:
            project_info: 项目信息

        Returns:
            创建的页面 ID，失败则返回 None
        """
        logger.info(f"创建新项目: {project_info['name']}")
        
        try:
            # 构造 Notion 页面属性
            properties = self._build_properties(project_info)
            
            # 创建页面
            url = f"{self.base_url}/pages"
            data = {
                "parent": {"database_id": self.database_id},
                "properties": properties
            }
            
            response = requests.post(url, headers=self.headers, json=data)
            
            if response.status_code != 200:
                logger.error(f"创建项目失败: {response.status_code} - {response.text}")
                return None
            
            page_id = response.json().get("id")
            logger.info(f"项目创建成功: {project_info['name']} (ID: {page_id})")
            return page_id
            
        except Exception as e:
            logger.error(f"创建项目时出错: {project_info['name']} - {str(e)}")
            return None
    
    def update_project(self, page_id: str, project_info: Dict[str, Any]) -> bool:
        """更新 Notion 中的已有项目

        Args:
            page_id: 页面 ID
            project_info: 更新后的项目信息

        Returns:
            是否更新成功
        """
        logger.info(f"更新项目: {project_info['name']}")
        
        try:
            # 构造 Notion 页面属性
            properties = self._build_properties(project_info)
            
            # 更新页面
            url = f"{self.base_url}/pages/{page_id}"
            data = {"properties": properties}
            
            response = requests.patch(url, headers=self.headers, json=data)
            
            if response.status_code != 200:
                logger.error(f"更新项目失败: {response.status_code} - {response.text}")
                return False
            
            logger.info(f"项目更新成功: {project_info['name']}")
            return True
            
        except Exception as e:
            logger.error(f"更新项目时出错: {project_info['name']} - {str(e)}")
            return False
    
    def _build_properties(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
        """构建 Notion 页面属性

        Args:
            project_info: 项目信息

        Returns:
            Notion 属性字典
        """
        properties = {
            "名称": {
                "title": [
                    {
                        "text": {
                            "content": project_info["name"]
                        }
                    }
                ]
            },
            "路径": {
                "rich_text": [
                    {
                        "text": {
                            "content": project_info["path"]
                        }
                    }
                ]
            },
            "技术栈": {
                "multi_select": [
                    {"name": tech} for tech in project_info["tech_stack"]
                ]
            },
            "项目类型": {
                "select": {
                    "name": project_info["project_type"]
                }
            },
            "状态": {
                "select": {
                    "name": project_info["status"]
                }
            },
            "优先级": {
                "select": {
                    "name": project_info["priority"]
                }
            },
            "描述": {
                "rich_text": [
                    {
                        "text": {
                            "content": project_info["description"]
                        }
                    }
                ]
            },
            "最后修改日期": {
                "date": {
                    "start": project_info["last_modified"]
                }
            }
        }
        
        return properties


def load_existing_projects() -> Dict[str, str]:
    """从 Notion 数据库加载已存在项目的工具函数

    Returns:
        项目名称到页面 ID 的映射
    """
    client = NotionClient(NOTION_API_KEY, NOTION_DATABASE_ID)
    return client.load_existing_projects()


def create_project(project_info: Dict[str, Any]) -> Optional[str]:
    """创建新 Notion 页面的工具函数

    Args:
        project_info: 项目信息

    Returns:
        创建的页面 ID，失败则返回 None
    """
    client = NotionClient(NOTION_API_KEY, NOTION_DATABASE_ID)
    return client.create_project(project_info)


def update_project(page_id: str, project_info: Dict[str, Any]) -> bool:
    """更新已有 Notion 页面的工具函数

    Args:
        page_id: 页面 ID
        project_info: 更新后的项目信息

    Returns:
        是否更新成功
    """
    client = NotionClient(NOTION_API_KEY, NOTION_DATABASE_ID)
    return client.update_project(page_id, project_info)


def sync_projects(projects_info: List[Dict[str, Any]]) -> Dict[str, Any]:
    """批量同步项目信息到 Notion

    Args:
        projects_info: 项目信息列表

    Returns:
        同步结果统计
    """
    logger.info(f"开始同步 {len(projects_info)} 个项目到 Notion...")
    
    # 初始化 Notion 客户端
    client = NotionClient(NOTION_API_KEY, NOTION_DATABASE_ID)
    
    # 加载已存在项目
    existing_projects = client.load_existing_projects()
    
    # 统计信息
    stats = {
        "total": len(projects_info),
        "created": 0,
        "updated": 0,
        "failed": 0,
        "skipped": 0
    }
    
    # 同步每个项目
    for project_info in projects_info:
        project_name = project_info["name"]
        
        # 检查是否已存在
        if project_name in existing_projects:
            # 更新已有项目
            page_id = existing_projects[project_name]
            success = client.update_project(page_id, project_info)
            
            if success:
                stats["updated"] += 1
            else:
                stats["failed"] += 1
        else:
            # 创建新项目
            page_id = client.create_project(project_info)
            
            if page_id:
                stats["created"] += 1
            else:
                stats["failed"] += 1
        
        # 添加延迟，避免 API 限流
        time.sleep(0.5)
    
    # 记录同步结果
    logger.info(f"同步完成. 总计: {stats['total']}, "
                f"新建: {stats['created']}, "
                f"更新: {stats['updated']}, "
                f"失败: {stats['failed']}, "
                f"跳过: {stats['skipped']}")
    
    return stats
