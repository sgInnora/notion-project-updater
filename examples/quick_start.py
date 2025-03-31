#!/usr/bin/env python3
"""
Notion 项目更新器 - 快速开始示例

这个脚本演示了如何使用 Notion 项目更新器的基本功能。
"""

import os
import sys
from pathlib import Path

# 确保可以导入主模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCAN_DIR
from analyzer import get_projects, analyze_project
from notion_client import sync_projects

def main():
    """快速开始示例主函数"""
    print(f"扫描目录: {SCAN_DIR}")
    
    # 获取项目列表
    projects = get_projects(SCAN_DIR)
    print(f"找到 {len(projects)} 个项目")
    
    # 限制为前 3 个项目（演示用）
    if len(projects) > 3:
        projects = projects[:3]
        print(f"为了演示，仅分析前 3 个项目")
    
    # 分析项目
    project_info_list = []
    for project in projects:
        print(f"分析项目: {project.name}")
        info = analyze_project(project)
        project_info_list.append(info)
        
        # 打印分析结果
        print(f"  技术栈: {', '.join(info['tech_stack'])}")
        print(f"  项目类型: {info['project_type']}")
        print(f"  状态: {info['status']}")
        print(f"  优先级: {info['priority']}")
        print(f"  最后修改: {info['last_modified']}")
        print("  描述:", info['description'][:100] + "..." if len(info['description']) > 100 else info['description'])
        print()
    
    # 询问是否同步到 Notion
    answer = input("是否将这些项目同步到 Notion? (y/n): ")
    if answer.lower() == 'y':
        print("正在同步到 Notion...")
        result = sync_projects(project_info_list)
        print(f"同步完成! 创建: {result['created']}, 更新: {result['updated']}, 失败: {result['failed']}")
    else:
        print("跳过同步到 Notion")

if __name__ == "__main__":
    main()
