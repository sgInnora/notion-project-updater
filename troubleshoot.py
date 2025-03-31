#!/usr/bin/env python3
"""
Notion 项目更新器 - 故障排除工具
"""

import os
import sys
import requests
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建控制台
console = Console()

def check_env_file():
    """检查环境变量文件"""
    env_path = Path(".env")
    
    if not env_path.exists():
        console.print("[bold red]错误: .env 文件不存在[/bold red]")
        console.print("尝试从 .env.example 创建 .env 文件")
        
        if Path(".env.example").exists():
            with open(".env.example", "r", encoding="utf-8") as src:
                with open(".env", "w", encoding="utf-8") as dst:
                    dst.write(src.read())
            console.print("[bold green]成功创建 .env 文件[/bold green]")
        else:
            console.print("[bold red]错误: .env.example 文件也不存在[/bold red]")
            return False
    
    # 检查 env 文件内容
    with open(".env", "r", encoding="utf-8") as f:
        env_content = f.read()
    
    if "your-secret-api-key" in env_content or "your-database-id" in env_content:
        console.print("[bold yellow]警告: .env 文件包含默认值，尚未配置[/bold yellow]")
        return False
    
    return True

def check_notion_credentials():
    """检查 Notion API 凭证"""
    api_key = os.environ.get("NOTION_API_KEY")
    database_id = os.environ.get("NOTION_DATABASE_ID")
    
    if not api_key or api_key == "your-secret-api-key":
        console.print("[bold red]错误: Notion API 密钥未设置或使用了默认值[/bold red]")
        return False
    
    if not database_id or database_id == "your-database-id":
        console.print("[bold red]错误: Notion 数据库 ID 未设置或使用了默认值[/bold red]")
        return False
    
    # 测试 API 连接
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    try:
        response = requests.get(
            f"https://api.notion.com/v1/databases/{database_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            console.print("[bold green]✓ Notion API 连接成功[/bold green]")
            return True
        else:
            console.print(f"[bold red]错误: Notion API 请求失败 ({response.status_code})[/bold red]")
            console.print(response.text)
            return False
    except Exception as e:
        console.print(f"[bold red]错误: Notion API 连接异常: {str(e)}[/bold red]")
        return False

def check_dependencies():
    """检查依赖项"""
    required_packages = [
        "requests",
        "gitpython",
        "pathlib",
        "schedule",
        "loguru",
        "rich",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        console.print("[bold red]错误: 缺少以下依赖包:[/bold red]")
        for package in missing_packages:
            console.print(f"  - {package}")
        
        install = Confirm.ask("是否尝试安装缺失的依赖?")
        if install:
            import subprocess
            try:
                for package in missing_packages:
                    console.print(f"安装 {package}...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                console.print("[bold green]✓ 所有依赖已安装[/bold green]")
                return True
            except Exception as e:
                console.print(f"[bold red]安装依赖时出错: {str(e)}[/bold red]")
                return False
        return False
    
    console.print("[bold green]✓ 所有依赖已安装[/bold green]")
    return True

def check_scan_directory():
    """检查扫描目录"""
    from config import SCAN_DIR
    
    if not SCAN_DIR.exists():
        console.print(f"[bold red]错误: 扫描目录不存在: {SCAN_DIR}[/bold red]")
        return False
    
    if not SCAN_DIR.is_dir():
        console.print(f"[bold red]错误: 扫描路径不是一个目录: {SCAN_DIR}[/bold red]")
        return False
    
    # 检查目录中的项目数量
    projects = [p for p in SCAN_DIR.iterdir() if p.is_dir() and not p.name.startswith('.')]
    
    if not projects:
        console.print(f"[bold yellow]警告: 扫描目录 {SCAN_DIR} 中没有找到任何项目[/bold yellow]")
        return False
    
    console.print(f"[bold green]✓ 扫描目录有效，包含 {len(projects)} 个潜在项目[/bold green]")
    return True

def run_quick_test():
    """运行快速测试"""
    console.print("\n[bold]正在运行快速测试...[/bold]")
    
    # 导入必要模块
    try:
        from config import SCAN_DIR
        from analyzer import get_projects, analyze_project
        
        # 获取一个项目进行测试
        projects = get_projects(SCAN_DIR)
        
        if not projects:
            console.print("[bold yellow]警告: 没有找到任何项目用于测试[/bold yellow]")
            return
        
        test_project = projects[0]
        console.print(f"使用项目进行测试: [cyan]{test_project.name}[/cyan]")
        
        # 分析项目
        info = analyze_project(test_project)
        
        # 显示分析结果
        table = Table(title=f"项目分析结果: {test_project.name}")
        table.add_column("属性", style="cyan")
        table.add_column("值", style="green")
        
        table.add_row("名称", info["name"])
        table.add_row("技术栈", ", ".join(info["tech_stack"]))
        table.add_row("项目类型", info["project_type"])
        table.add_row("状态", info["status"])
        table.add_row("优先级", info["priority"])
        table.add_row("最后修改日期", info["last_modified"])
        table.add_row("描述", info["description"][:100] + "..." if len(info["description"]) > 100 else info["description"])
        
        console.print(table)
        console.print("[bold green]✓ 项目分析功能正常[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]测试时出错: {str(e)}[/bold red]")

def update_config():
    """更新配置"""
    console.print("\n[bold]更新配置[/bold]")
    
    # 更新 Notion API 密钥
    update_api_key = Confirm.ask("是否更新 Notion API 密钥?")
    if update_api_key:
        api_key = Prompt.ask("请输入 Notion API 密钥", password=True)
        os.environ["NOTION_API_KEY"] = api_key
        
        # 更新 .env 文件
        with open(".env", "r", encoding="utf-8") as f:
            env_content = f.read()
        
        if "NOTION_API_KEY=" in env_content:
            env_content = env_content.replace(
                f"NOTION_API_KEY={os.environ.get('NOTION_API_KEY', 'your-secret-api-key')}",
                f"NOTION_API_KEY={api_key}"
            )
        else:
            env_content += f"\nNOTION_API_KEY={api_key}"
        
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        console.print("[bold green]✓ API 密钥已更新[/bold green]")
    
    # 更新数据库 ID
    update_db_id = Confirm.ask("是否更新 Notion 数据库 ID?")
    if update_db_id:
        db_id = Prompt.ask("请输入 Notion 数据库 ID")
        os.environ["NOTION_DATABASE_ID"] = db_id
        
        # 更新 .env 文件
        with open(".env", "r", encoding="utf-8") as f:
            env_content = f.read()
        
        if "NOTION_DATABASE_ID=" in env_content:
            env_content = env_content.replace(
                f"NOTION_DATABASE_ID={os.environ.get('NOTION_DATABASE_ID', 'your-database-id')}",
                f"NOTION_DATABASE_ID={db_id}"
            )
        else:
            env_content += f"\nNOTION_DATABASE_ID={db_id}"
        
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        console.print("[bold green]✓ 数据库 ID 已更新[/bold green]")
    
    # 更新扫描目录
    update_scan_dir = Confirm.ask("是否更新扫描目录?")
    if update_scan_dir:
        scan_dir = Prompt.ask("请输入扫描目录路径")
        
        # 更新 config.py 文件
        with open("config.py", "r", encoding="utf-8") as f:
            config_content = f.read()
        
        config_content = config_content.replace(
            'SCAN_DIR = Path("/Users/anwu/Documents/code")',
            f'SCAN_DIR = Path("{scan_dir}")'
        )
        
        with open("config.py", "w", encoding="utf-8") as f:
            f.write(config_content)
        
        console.print("[bold green]✓ 扫描目录已更新[/bold green]")

def main():
    """主函数"""
    console.print(Panel.fit(
        "[bold cyan]Notion 项目更新器 - 故障排除工具[/bold cyan]\n\n"
        "这个工具将帮助你检查和解决常见问题",
        title="欢迎"
    ))
    
    # 检查环境文件
    console.print("\n[bold]1. 检查环境文件[/bold]")
    env_check = check_env_file()
    
    # 检查 Notion 凭证
    console.print("\n[bold]2. 检查 Notion API 凭证[/bold]")
    cred_check = check_notion_credentials()
    
    # 检查依赖项
    console.print("\n[bold]3. 检查依赖项[/bold]")
    dep_check = check_dependencies()
    
    # 检查扫描目录
    console.print("\n[bold]4. 检查扫描目录[/bold]")
    dir_check = check_scan_directory()
    
    # 运行快速测试
    if dep_check and dir_check:
        run_quick_test()
    
    # 显示诊断结果
    console.print("\n[bold]诊断结果[/bold]")
    table = Table()
    table.add_column("检查项", style="cyan")
    table.add_column("状态", style="bold")
    
    table.add_row("环境文件", "[green]通过[/green]" if env_check else "[red]失败[/red]")
    table.add_row("Notion API 凭证", "[green]通过[/green]" if cred_check else "[red]失败[/red]")
    table.add_row("依赖项", "[green]通过[/green]" if dep_check else "[red]失败[/red]")
    table.add_row("扫描目录", "[green]通过[/green]" if dir_check else "[red]失败[/red]")
    
    console.print(table)
    
    # 如果存在问题，提供更新配置选项
    if not (env_check and cred_check and dep_check and dir_check):
        fix = Confirm.ask("是否尝试解决检测到的问题?")
        if fix:
            update_config()
    
    # 总结
    console.print(Panel.fit(
        "[bold green]故障排除完成![/bold green]\n\n"
        "如果所有检查都通过，你可以运行 [cyan]python main.py[/cyan] 开始使用项目更新器。\n"
        "如果仍有问题，请参考 README.md 文件获取更多信息。",
        title="完成"
    ))

if __name__ == "__main__":
    main()
