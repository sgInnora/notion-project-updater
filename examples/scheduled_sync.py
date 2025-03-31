#!/usr/bin/env python3
"""
Notion 项目更新器 - 定时同步示例

这个示例演示了如何设置定时同步任务。
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

# 确保可以导入主模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCAN_DIR
from analyzer import get_projects, analyze_project
from notion_client import sync_projects
from scheduler import run_scheduler

def sync_task():
    """同步任务"""
    print(f"\n--- 开始同步 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    
    try:
        # 扫描项目
        projects = get_projects(SCAN_DIR)
        print(f"找到 {len(projects)} 个项目")
        
        # 分析项目
        project_info_list = []
        for i, project in enumerate(projects):
            print(f"[{i+1}/{len(projects)}] 分析项目: {project.name}")
            info = analyze_project(project)
            project_info_list.append(info)
        
        # 同步到 Notion
        print(f"同步 {len(project_info_list)} 个项目到 Notion...")
        results = sync_projects(project_info_list)
        
        print(f"同步完成! 总计: {results['total']}, 新建: {results['created']}, " 
              f"更新: {results['updated']}, 失败: {results['failed']}")
              
    except Exception as e:
        print(f"同步任务出错: {str(e)}")
    
    print(f"--- 同步结束 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---\n")
    return True

def simulate_schedule(interval_minutes=1, iterations=3):
    """模拟定时执行（仅用于演示）
    
    Args:
        interval_minutes: 间隔时间（分钟）
        iterations: 执行次数
    """
    print(f"模拟定时执行，间隔 {interval_minutes} 分钟，共执行 {iterations} 次")
    
    for i in range(iterations):
        print(f"执行第 {i+1} 次同步...")
        sync_task()
        
        if i < iterations - 1:
            next_time = datetime.now().timestamp() + interval_minutes * 60
            next_time_str = datetime.fromtimestamp(next_time).strftime('%H:%M:%S')
            
            print(f"等待下一次执行 (将在 {next_time_str} 执行)...")
            time.sleep(interval_minutes * 60)

def main():
    """定时同步示例主函数"""
    print("Notion 项目更新器 - 定时同步示例")
    print("==================================")
    
    print("\n有三种方式运行定时同步:")
    print("1. 模拟定时执行（用于示例，每分钟执行一次，共执行3次）")
    print("2. 实际定时执行（每小时执行一次，无限循环）")
    print("3. 执行一次然后退出")
    
    choice = input("\n请选择运行方式 (1/2/3): ")
    
    if choice == '1':
        # 模拟定时执行
        simulate_schedule(interval_minutes=1, iterations=3)
    elif choice == '2':
        # 实际定时执行
        print("启动定时执行，每小时执行一次...")
        print("按 Ctrl+C 停止")
        
        # 先执行一次
        sync_task()
        
        # 然后启动调度器
        run_scheduler(sync_task, interval_hours=1)
    else:
        # 执行一次
        print("执行一次同步任务...")
        sync_task()

if __name__ == "__main__":
    main()
