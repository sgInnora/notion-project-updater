#!/usr/bin/env python3
"""
Notion 项目更新器 - 自定义分析器示例

这个示例演示了如何创建和使用自定义项目分析器。
"""

import os
import sys
from pathlib import Path

# 确保可以导入主模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import SCAN_DIR
from analyzer import get_projects
from notion_client import sync_projects

def custom_project_analyzer(project_path):
    """自定义项目分析器
    
    这个分析器会添加一些额外的自定义字段
    
    Args:
        project_path: 项目路径
        
    Returns:
        项目信息字典
    """
    # 导入标准分析器
    from analyzer import analyze_project
    
    # 先使用标准分析器获取基本信息
    project_info = analyze_project(project_path)
    
    # 添加自定义信息
    
    # 1. 计算项目大小（MB）
    total_size = 0
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                total_size += os.path.getsize(file_path)
            except:
                pass
    
    project_info['size_mb'] = round(total_size / (1024 * 1024), 2)
    
    # 2. 计算文件数量
    file_count = sum(len(files) for _, _, files in os.walk(project_path))
    project_info['file_count'] = file_count
    
    # 3. 计算代码行数（简易版，仅计算部分文件类型）
    code_extensions = ['.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.css', '.java', '.c', '.cpp', '.go', '.rs']
    line_count = 0
    
    for root, _, files in os.walk(project_path):
        for file in files:
            if any(file.endswith(ext) for ext in code_extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        line_count += len(f.readlines())
                except:
                    pass
    
    project_info['code_lines'] = line_count
    
    # 4. 定制项目复杂度评分 (0-100)
    # 简单算法: 基于文件数、代码行数和技术栈数量
    complexity = min(100, (
        (file_count / 100) * 20 +  # 文件数贡献
        (line_count / 5000) * 40 +  # 代码行数贡献
        (len(project_info['tech_stack']) / 4) * 40  # 技术栈多样性贡献
    ))
    
    project_info['complexity'] = round(complexity)
    
    # 返回增强后的项目信息
    return project_info

def main():
    """自定义分析器示例主函数"""
    print(f"扫描目录: {SCAN_DIR}")
    
    # 获取项目列表
    projects = get_projects(SCAN_DIR)
    print(f"找到 {len(projects)} 个项目")
    
    # 限制为前 3 个项目（演示用）
    if len(projects) > 3:
        projects = projects[:3]
        print(f"为了演示，仅分析前 3 个项目")
    
    # 使用自定义分析器分析项目
    project_info_list = []
    for project in projects:
        print(f"使用自定义分析器分析项目: {project.name}")
        info = custom_project_analyzer(project)
        project_info_list.append(info)
        
        # 打印标准分析结果
        print(f"  技术栈: {', '.join(info['tech_stack'])}")
        print(f"  项目类型: {info['project_type']}")
        print(f"  状态: {info['status']}")
        
        # 打印自定义分析结果
        print(f"  项目大小: {info['size_mb']} MB")
        print(f"  文件数量: {info['file_count']}")
        print(f"  代码行数: {info['code_lines']}")
        print(f"  复杂度评分: {info['complexity']}/100")
        print()
    
    # 询问是否同步到 Notion
    print("注意: 要将自定义字段同步到 Notion，你需要在 Notion 数据库中添加对应的字段")
    print("      比如 '项目大小'、'文件数量'、'代码行数'、'复杂度评分' 等")
    
    answer = input("是否将这些项目同步到 Notion? (y/n): ")
    if answer.lower() == 'y':
        print("正在同步到 Notion...")
        # 注意：如要同步自定义字段，你需要修改 notion_client.py 中的 _build_properties 方法
        result = sync_projects(project_info_list)
        print(f"同步完成! 创建: {result['created']}, 更新: {result['updated']}, 失败: {result['failed']}")
    else:
        print("跳过同步到 Notion")

if __name__ == "__main__":
    main()
