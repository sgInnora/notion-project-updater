# main.py
"""
项目主程序入口
"""

import os
import argparse
import sys
from pathlib import Path
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from config import SCAN_DIR, LOG_FILE
from analyzer import get_projects, analyze_project
from notion_client import sync_projects
from scheduler import run_scheduler, run_at_specific_time, run_with_cron_expression


# 配置日志
logger.remove()  # 移除默认处理器
logger.add(sys.stderr, level="INFO")  # 添加标准错误输出处理器
logger.add(LOG_FILE, rotation="500 MB", level="DEBUG")  # 添加文件处理器


def execute_sync():
    """执行项目同步"""
    console = Console()
    
    with console.status("[bold green]扫描项目目录...") as status:
        # 扫描项目
        project_paths = get_projects(SCAN_DIR)
        
        if not project_paths:
            logger.error(f"没有在 {SCAN_DIR} 找到任何项目")
            console.print(f"[bold red]错误：没有在 {SCAN_DIR} 找到任何项目[/bold red]")
            return
        
        status.update(f"[bold green]正在分析 {len(project_paths)} 个项目...")
        
        # 分析项目
        projects_info = []
        for i, project_path in enumerate(project_paths):
            status.update(f"[bold green]正在分析项目 ({i+1}/{len(project_paths)}): {project_path.name}")
            project_info = analyze_project(project_path)
            projects_info.append(project_info)
        
        status.update(f"[bold green]正在同步 {len(projects_info)} 个项目到 Notion...")
        
        # 同步到 Notion
        result = sync_projects(projects_info)
    
    # 显示同步结果
    table = Table(title="同步结果")
    table.add_column("类型", style="cyan")
    table.add_column("数量", style="magenta")
    
    table.add_row("总计项目", str(result["total"]))
    table.add_row("新建项目", str(result["created"]))
    table.add_row("更新项目", str(result["updated"]))
    table.add_row("失败项目", str(result["failed"]))
    table.add_row("跳过项目", str(result["skipped"]))
    
    console.print(table)
    console.print(Panel.fit(
        "[bold green]同步完成！[/bold green] 详细日志请查看: " + str(LOG_FILE),
        title="Notion 项目更新器"
    ))


def main():
    """主程序入口"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Notion 项目更新器 - 自动扫描并同步代码项目到 Notion 数据库")
    
    parser.add_argument("--schedule", action="store_true", help="启动定时运行模式")
    parser.add_argument("--interval", type=int, default=24, help="执行间隔（小时）")
    parser.add_argument("--time", type=str, help="每天固定执行时间（格式：HH:MM）")
    parser.add_argument("--cron", type=str, help="使用 cron 表达式设置执行计划")
    
    args = parser.parse_args()
    
    # 创建控制台
    console = Console()
    
    # 显示欢迎信息
    console.print(Panel.fit(
        "[bold cyan]Notion 项目更新器[/bold cyan]\n\n"
        f"将扫描 [bold yellow]{SCAN_DIR}[/bold yellow] 目录下的所有代码项目\n"
        "并自动同步到 Notion 数据库",
        title="欢迎"
    ))
    
    # 检查 API 配置
    if os.environ.get("NOTION_API_KEY") == "your-secret-api-key" or os.environ.get("NOTION_DATABASE_ID") == "your-database-id":
        console.print("[bold red]警告：尚未配置 Notion API 密钥或数据库 ID[/bold red]")
        console.print("请在 .env 文件中设置 NOTION_API_KEY 和 NOTION_DATABASE_ID 环境变量")
        return
    
    # 检查扫描目录
    if not SCAN_DIR.exists() or not SCAN_DIR.is_dir():
        console.print(f"[bold red]错误：扫描目录不存在或不是一个有效的目录: {SCAN_DIR}[/bold red]")
        return
    
    # 执行同步或启动调度器
    if args.schedule:
        if args.time:
            try:
                hour, minute = map(int, args.time.split(':'))
                console.print(f"[bold green]启动定时运行模式，将在每天 {hour:02d}:{minute:02d} 执行[/bold green]")
                run_at_specific_time(execute_sync, hour, minute)
            except ValueError:
                console.print("[bold red]错误：时间格式无效，请使用 HH:MM 格式[/bold red]")
                return
        elif args.cron:
            console.print(f"[bold green]启动定时运行模式，cron 表达式: {args.cron}[/bold green]")
            run_with_cron_expression(execute_sync, args.cron)
        else:
            interval = args.interval
            console.print(f"[bold green]启动定时运行模式，每 {interval} 小时执行一次[/bold green]")
            # 先执行一次
            execute_sync()
            # 然后启动调度器
            run_scheduler(execute_sync, interval)
    else:
        # 立即执行同步
        execute_sync()


if __name__ == "__main__":
    main()
