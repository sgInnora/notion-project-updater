# analyzer.py
"""
项目分析模块，用于扫描项目文件夹并提取项目信息
"""

import os
import re
import time
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import git
from loguru import logger

from config import (
    SCAN_DIR, 
    TECH_STACK_MARKERS, 
    PROJECT_TYPE_MARKERS,
    GIT_ACTIVE_THRESHOLD_DAYS,
    GIT_MAINTENANCE_THRESHOLD_DAYS,
    PRIORITY_THRESHOLDS
)


def get_projects(scan_dir: Path) -> List[Path]:
    """获取指定目录下的所有项目文件夹

    Args:
        scan_dir: 要扫描的目录路径

    Returns:
        项目文件夹路径列表
    """
    logger.info(f"扫描目录: {scan_dir}")
    
    if not scan_dir.exists() or not scan_dir.is_dir():
        logger.error(f"扫描目录不存在或不是一个有效的目录: {scan_dir}")
        return []
    
    # 获取所有子目录（排除隐藏文件夹和非目录）
    projects = [
        item for item in scan_dir.iterdir() 
        if item.is_dir() and not item.name.startswith('.')
    ]
    
    logger.info(f"找到 {len(projects)} 个潜在项目")
    return projects


def detect_tech_stack(project_path: Path) -> List[str]:
    """检测项目使用的技术栈

    Args:
        project_path: 项目路径

    Returns:
        检测到的技术栈列表
    """
    tech_stacks = []
    
    # 获取所有文件（包括子目录）的扩展名和文件名
    all_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            all_files.append(os.path.join(root, file))
    
    # 检查项目目录中的所有文件
    file_content = "\n".join(all_files).lower()
    
    # 检查每个技术栈的标记
    for tech, markers in TECH_STACK_MARKERS.items():
        for marker in markers:
            if marker.startswith('.'):  # 检查文件扩展名
                if any(f.endswith(marker) for f in all_files):
                    tech_stacks.append(tech)
                    break
            else:  # 检查文件名或内容
                if marker.lower() in file_content:
                    tech_stacks.append(tech)
                    break
    
    # 去重
    tech_stacks = list(set(tech_stacks))
    return tech_stacks


def detect_project_type(project_path: Path, tech_stack: List[str]) -> str:
    """根据项目特征和技术栈推断项目类型

    Args:
        project_path: 项目路径
        tech_stack: 检测到的技术栈

    Returns:
        项目类型
    """
    # 获取所有文件名进行类型检测
    all_files = []
    for root, dirs, files in os.walk(project_path):
        all_files.extend(files)
        all_files.extend(dirs)
    
    file_content = "\n".join(all_files).lower()
    tech_content = "\n".join(tech_stack).lower()
    
    # 检查每种项目类型的标记
    for project_type, markers in PROJECT_TYPE_MARKERS.items():
        for marker in markers:
            if marker.lower() in file_content or marker.lower() in tech_content:
                return project_type
    
    # 根据技术栈做兜底推断
    if "Flask" in tech_stack or "Django" in tech_stack or "Express" in tech_stack:
        return "Web应用"
    elif "React" in tech_stack or "Vue" in tech_stack or "Angular" in tech_stack:
        return "Web应用"
    elif "TensorFlow" in tech_stack or "PyTorch" in tech_stack or "机器学习" in tech_stack:
        return "机器学习"
    elif "Flutter" in tech_stack or "React Native" in tech_stack:
        return "移动应用"
    elif "Python" in tech_stack and ("pandas" in file_content or "numpy" in file_content):
        return "数据分析"
    
    # 默认类型
    return "其他"


def detect_project_status(project_path: Path) -> str:
    """检测项目状态（活跃、维护中、暂停）

    Args:
        project_path: 项目路径

    Returns:
        项目状态
    """
    try:
        # 尝试将项目作为Git仓库打开
        repo = git.Repo(project_path)
        
        # 获取最近一次提交的时间
        commits = list(repo.iter_commits(max_count=5))
        if not commits:
            # 没有提交记录，使用文件修改时间
            return detect_status_by_file_time(project_path)
        
        last_commit_time = commits[0].committed_datetime
        now = datetime.datetime.now(last_commit_time.tzinfo)
        days_since_last_commit = (now - last_commit_time).days
        
        if days_since_last_commit <= GIT_ACTIVE_THRESHOLD_DAYS:
            return "活跃"
        elif days_since_last_commit <= GIT_MAINTENANCE_THRESHOLD_DAYS:
            return "维护中"
        else:
            return "暂停"
            
    except (git.InvalidGitRepositoryError, git.NoSuchPathError):
        # 不是Git仓库，使用文件修改时间
        return detect_status_by_file_time(project_path)


def detect_status_by_file_time(project_path: Path) -> str:
    """根据文件修改时间检测项目状态

    Args:
        project_path: 项目路径

    Returns:
        项目状态
    """
    newest_time = 0
    now = time.time()
    
    # 遍历所有文件，找出最新修改时间
    for root, _, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(file_path)
                newest_time = max(newest_time, mtime)
            except:
                continue
    
    if newest_time == 0:
        return "暂停"
    
    days_since_last_modified = (now - newest_time) / (24 * 3600)
    
    if days_since_last_modified <= GIT_ACTIVE_THRESHOLD_DAYS:
        return "活跃"
    elif days_since_last_modified <= GIT_MAINTENANCE_THRESHOLD_DAYS:
        return "维护中"
    else:
        return "暂停"


def detect_project_priority(project_path: Path, status: str) -> str:
    """基于项目状态和最后修改时间确定项目优先级

    Args:
        project_path: 项目路径
        status: 项目状态

    Returns:
        项目优先级（高、中、低）
    """
    if status == "活跃":
        # 活跃项目优先级较高
        return "高"
    
    # 找出最近修改时间
    newest_time = 0
    for root, _, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(file_path)
                newest_time = max(newest_time, mtime)
            except:
                continue
    
    if newest_time == 0:
        return "低"
    
    # 计算距今天数
    days_since_modified = (time.time() - newest_time) / (24 * 3600)
    
    # 根据修改时间判断优先级
    if days_since_modified <= PRIORITY_THRESHOLDS["高"]:
        return "高"
    elif days_since_modified <= PRIORITY_THRESHOLDS["中"]:
        return "中"
    else:
        return "低"


def extract_description(project_path: Path) -> str:
    """从项目中提取描述信息

    优先从 README 文件中提取，如果没有则生成一个基本描述

    Args:
        project_path: 项目路径

    Returns:
        项目描述
    """
    # 尝试从 README 文件中提取
    readme_files = [
        "README.md", "README.txt", "README", "readme.md", 
        "Readme.md", "readme.txt", "README.markdown"
    ]
    
    for readme in readme_files:
        readme_path = project_path / readme
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 尝试提取标题下的第一段作为描述
                    lines = content.split('\n')
                    description_lines = []
                    
                    # 跳过标题行
                    start_idx = 0
                    for i, line in enumerate(lines):
                        if line.startswith('#') or line.startswith('==='):
                            start_idx = i + 1
                            break
                    
                    # 提取第一个非空段落
                    current_paragraph = []
                    for line in lines[start_idx:]:
                        if line.strip() == '':
                            if current_paragraph:
                                description_lines = current_paragraph
                                break
                        else:
                            current_paragraph.append(line)
                    
                    if description_lines:
                        description = ' '.join(description_lines)
                        # 清理 Markdown 标记
                        description = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', description)  # 链接
                        description = re.sub(r'[*_]{1,2}([^*_]+)[*_]{1,2}', r'\1', description)  # 粗体/斜体
                        description = re.sub(r'`([^`]+)`', r'\1', description)  # 行内代码
                        
                        # 限制长度
                        if len(description) > 500:
                            description = description[:497] + '...'
                        
                        return description
            except:
                continue
    
    # 如果没有找到有效的 README，返回基本描述
    return f"位于 {project_path} 的项目"


def get_last_modified_date(project_path: Path) -> str:
    """获取项目最后修改日期

    Args:
        project_path: 项目路径

    Returns:
        格式化的日期字符串
    """
    try:
        # 尝试从 Git 获取
        repo = git.Repo(project_path)
        commits = list(repo.iter_commits(max_count=1))
        if commits:
            last_commit_time = commits[0].committed_datetime
            return last_commit_time.strftime("%Y-%m-%d")
    except:
        pass
    
    # 回退到文件系统时间
    newest_time = 0
    for root, _, files in os.walk(project_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(file_path)
                newest_time = max(newest_time, mtime)
            except:
                continue
    
    if newest_time > 0:
        return datetime.datetime.fromtimestamp(newest_time).strftime("%Y-%m-%d")
    else:
        return datetime.datetime.now().strftime("%Y-%m-%d")


def analyze_project(project_path: Path) -> Dict[str, Any]:
    """分析单个项目并返回分析结果

    Args:
        project_path: 项目路径

    Returns:
        包含项目信息的字典
    """
    logger.info(f"分析项目: {project_path.name}")
    
    try:
        # 检测技术栈
        tech_stack = detect_tech_stack(project_path)
        
        # 检测项目类型
        project_type = detect_project_type(project_path, tech_stack)
        
        # 检测项目状态
        status = detect_project_status(project_path)
        
        # 确定项目优先级
        priority = detect_project_priority(project_path, status)
        
        # 提取项目描述
        description = extract_description(project_path)
        
        # 获取最后修改日期
        last_modified = get_last_modified_date(project_path)
        
        # 组装项目信息
        project_info = {
            "name": project_path.name,
            "path": str(project_path),
            "tech_stack": tech_stack,
            "project_type": project_type,
            "status": status,
            "priority": priority,
            "description": description,
            "last_modified": last_modified,
        }
        
        logger.info(f"完成项目分析: {project_path.name}")
        return project_info
        
    except Exception as e:
        logger.error(f"分析项目时出错: {project_path.name} - {str(e)}")
        # 返回基本信息
        return {
            "name": project_path.name,
            "path": str(project_path),
            "tech_stack": [],
            "project_type": "未知",
            "status": "未知",
            "priority": "低",
            "description": f"无法分析此项目: {str(e)}",
            "last_modified": datetime.datetime.now().strftime("%Y-%m-%d"),
        }
