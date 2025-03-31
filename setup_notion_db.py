#!/usr/bin/env python3
"""
Notion 项目更新器 - 数据库初始化脚本

这个脚本用于在 Notion 中创建所需的数据库结构
"""

import os
import requests
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# 加载环境变量
load_dotenv()

# 创建控制台
console = Console()

def get_notion_credentials():
    """获取 Notion API 凭证"""
    api_key = os.environ.get("NOTION_API_KEY")
    
    if not api_key or api_key == "your-secret-api-key":
        console.print("[bold red]未找到有效的 Notion API 密钥[/bold red]")
        api_key = Prompt.ask("请输入你的 Notion API 密钥", password=True)
        
        # 保存到环境变量
        os.environ["NOTION_API_KEY"] = api_key
        
        # 更新 .env 文件
        with open(".env", "r", encoding="utf-8") as f:
            env_content = f.read()
        
        env_content = env_content.replace(
            "NOTION_API_KEY=your-secret-api-key", 
            f"NOTION_API_KEY={api_key}"
        )
        
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
    
    return api_key

def get_parent_page_id():
    """获取父页面ID"""
    console.print("\n[bold cyan]欢迎使用 Notion 项目更新器数据库初始化工具[/bold cyan]")
    console.print("这个工具将在你的 Notion 工作区中创建一个新的数据库。")
    console.print("你需要提供一个父页面 ID，新的数据库将在这个页面下创建。")
    
    console.print("\n[yellow]如何获取父页面 ID:[/yellow]")
    console.print("1. 在 Notion 中打开你想要添加数据库的页面")
    console.print("2. 从 URL 中复制页面 ID")
    console.print("   例如: https://www.notion.so/workspace/[bold]abcdef123456[/bold]?v=...")
    console.print("   其中 [bold]abcdef123456[/bold] 就是页面 ID")
    
    parent_id = Prompt.ask("\n请输入父页面 ID")
    
    # 去除可能存在的破折号
    parent_id = parent_id.replace("-", "")
    
    return parent_id

def create_notion_database(api_key, parent_id):
    """创建 Notion 数据库"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    # 数据库结构
    data = {
        "parent": {
            "type": "page_id",
            "page_id": parent_id
        },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": "代码项目管理",
                    "link": None
                }
            }
        ],
        "properties": {
            "名称": {
                "title": {}
            },
            "路径": {
                "rich_text": {}
            },
            "技术栈": {
                "multi_select": {
                    "options": [
                        {"name": "Python", "color": "blue"},
                        {"name": "JavaScript", "color": "yellow"},
                        {"name": "React", "color": "green"},
                        {"name": "Node.js", "color": "green"},
                        {"name": "Vue", "color": "green"},
                        {"name": "Go", "color": "blue"},
                        {"name": "Java", "color": "orange"},
                        {"name": "C/C++", "color": "gray"},
                        {"name": "Rust", "color": "orange"},
                        {"name": "PHP", "color": "purple"},
                        {"name": "Ruby", "color": "red"},
                        {"name": "Swift", "color": "orange"},
                        {"name": "Kotlin", "color": "purple"},
                        {"name": "TypeScript", "color": "blue"},
                        {"name": "Flutter/Dart", "color": "blue"},
                        {"name": "R", "color": "blue"},
                        {"name": "Shell", "color": "gray"},
                        {"name": "C#", "color": "purple"},
                        {"name": "HTML/CSS", "color": "orange"},
                        {"name": "Jupyter", "color": "orange"}
                    ]
                }
            },
            "项目类型": {
                "select": {
                    "options": [
                        {"name": "Web应用", "color": "blue"},
                        {"name": "CLI工具", "color": "gray"},
                        {"name": "服务端", "color": "green"},
                        {"name": "移动应用", "color": "purple"},
                        {"name": "库/框架", "color": "yellow"},
                        {"name": "机器学习", "color": "pink"},
                        {"name": "数据分析", "color": "orange"},
                        {"name": "游戏", "color": "red"},
                        {"name": "自动化脚本", "color": "brown"},
                        {"name": "区块链", "color": "blue"},
                        {"name": "其他", "color": "default"}
                    ]
                }
            },
            "状态": {
                "select": {
                    "options": [
                        {"name": "活跃", "color": "green"},
                        {"name": "维护中", "color": "yellow"},
                        {"name": "暂停", "color": "gray"}
                    ]
                }
            },
            "优先级": {
                "select": {
                    "options": [
                        {"name": "高", "color": "red"},
                        {"name": "中", "color": "yellow"},
                        {"name": "低", "color": "gray"}
                    ]
                }
            },
            "描述": {
                "rich_text": {}
            },
            "最后修改日期": {
                "date": {}
            }
        }
    }
    
    try:
        response = requests.post(
            "https://api.notion.com/v1/databases", 
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            database_id = result["id"]
            
            # 更新 .env 文件中的数据库 ID
            with open(".env", "r", encoding="utf-8") as f:
                env_content = f.read()
            
            env_content = env_content.replace(
                "NOTION_DATABASE_ID=your-database-id", 
                f"NOTION_DATABASE_ID={database_id}"
            )
            
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            
            console.print(f"\n[bold green]成功创建数据库！[/bold green]")
            console.print(f"数据库 ID: {database_id}")
            console.print("已自动更新 .env 文件")
            
            return database_id
        else:
            console.print(f"\n[bold red]创建数据库失败: {response.status_code}[/bold red]")
            console.print(response.text)
            return None
            
    except Exception as e:
        console.print(f"\n[bold red]创建数据库时出错: {str(e)}[/bold red]")
        return None

def main():
    """主函数"""
    console.print(Panel.fit(
        "[bold cyan]Notion 项目更新器 - 数据库初始化[/bold cyan]\n\n"
        "这个工具将帮助你在 Notion 中创建项目管理数据库",
        title="欢迎"
    ))
    
    # 获取 Notion API 凭证
    api_key = get_notion_credentials()
    
    # 获取父页面 ID
    parent_id = get_parent_page_id()
    
    # 创建数据库
    console.print("\n[bold]正在创建数据库...[/bold]")
    database_id = create_notion_database(api_key, parent_id)
    
    if database_id:
        console.print(Panel.fit(
            f"[bold green]设置完成！[/bold green]\n\n"
            f"已在你的 Notion 工作区创建数据库，并更新了配置文件。\n"
            f"现在你可以运行 [bold]python main.py[/bold] 开始使用项目更新器。",
            title="成功"
        ))
    else:
        console.print(Panel.fit(
            "[bold red]设置失败[/bold red]\n\n"
            "请检查你的 Notion API 密钥和父页面 ID 是否正确。\n"
            "确保你的 Notion 集成有足够的权限。",
            title="错误"
        ))

if __name__ == "__main__":
    main()
