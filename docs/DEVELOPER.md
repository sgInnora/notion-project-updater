# Notion 项目更新器 - 开发者文档

本文档提供了 Notion 项目更新器的技术细节和架构信息，帮助开发者理解项目结构和核心组件。

## 目录

- [项目架构](#项目架构)
- [核心模块](#核心模块)
  - [主程序 (main.py)](#主程序-mainpy)
  - [配置管理 (config.py)](#配置管理-configpy)
  - [项目分析器 (analyzer.py)](#项目分析器-analyzerpy)
  - [Notion 客户端 (notion_client.py)](#notion-客户端-notion_clientpy)
  - [调度器 (scheduler.py)](#调度器-schedulerpy)
- [数据流](#数据流)
- [扩展指南](#扩展指南)
  - [添加新的分析维度](#添加新的分析维度)
  - [修改 Notion 集成](#修改-notion-集成)
  - [实现自定义调度策略](#实现自定义调度策略)
- [API 文档](#api-文档)
- [测试策略](#测试策略)

## 项目架构

Notion 项目更新器采用模块化架构设计，每个模块负责特定功能，降低了组件间的耦合度。整体架构如下：

```
+----------------+       +----------------+       +----------------+
|                |       |                |       |                |
|     Scanner    +------>+    Analyzer    +------>+  Notion Client |
|                |       |                |       |                |
+----------------+       +----------------+       +----------------+
        ^                        ^                        ^
        |                        |                        |
        v                        v                        v
+----------------+       +----------------+       +----------------+
|                |       |                |       |                |
|    Scheduler   |<------+  Configuration +------>+     Logger     |
|                |       |                |       |                |
+----------------+       +----------------+       +----------------+
```

这种设计允许独立开发和测试各个组件，同时确保它们能够协同工作。

## 核心模块

### 主程序 (main.py)

`main.py` 是应用程序的入口点，负责：

- 解析命令行参数
- 初始化其他模块
- 协调扫描、分析和同步过程
- 处理调度逻辑

关键函数：

- `execute_sync()`: 执行完整的同步流程
- `main()`: 程序入口，处理命令行参数

### 配置管理 (config.py)

`config.py` 管理所有全局配置，包括：

- 环境变量和常量
- 扫描目录设置
- 技术栈和项目类型检测规则
- 日志配置

配置值由以下来源提供：

1. 硬编码的默认值
2. 环境变量
3. 命令行参数（通过 `main.py` 处理）

### 项目分析器 (analyzer.py)

`analyzer.py` 包含项目扫描和分析逻辑，负责：

- 扫描目录获取项目列表
- 分析每个项目的特征
- 提取项目信息

主要组件：

- `get_projects()`: 获取项目列表
- `analyze_project()`: 综合分析单个项目
- 多个专用检测函数（如 `detect_tech_stack()`, `detect_project_type()` 等）

扩展分析器只需实现与 `analyze_project()` 相同的接口，即可轻松集成。

### Notion 客户端 (notion_client.py)

`notion_client.py` 处理与 Notion API 的所有交互，包括：

- 查询现有项目
- 创建新项目页面
- 更新已有项目页面
- 处理数据格式转换

主要组件：

- `NotionClient` 类：封装 API 操作
- `sync_projects()`: 批量同步项目信息
- `_build_properties()`: 构建 Notion 页面属性

该模块使用官方 Notion API，支持完整的 CRUD 操作。

### 调度器 (scheduler.py)

`scheduler.py` 提供定时执行功能，包括：

- 基于时间间隔的调度
- 特定时间执行
- Cron 表达式支持

主要组件：

- `run_scheduler()`: 基本调度器
- `run_at_specific_time()`: 特定时间执行
- `run_with_cron_expression()`: Cron 表达式支持

## 数据流

数据在系统中的流动路径如下：

1. **扫描阶段**：
   - `main.py` 调用 `get_projects()` 获取项目路径列表
   - 返回：`List[Path]`

2. **分析阶段**：
   - 对每个项目路径调用 `analyze_project()`
   - 返回：`Dict[str, Any]` 包含项目信息

3. **同步阶段**：
   - 调用 `sync_projects()` 传入项目信息列表
   - 内部调用 Notion API
   - 返回：同步统计信息

4. **调度阶段**（如启用）：
   - 调度器根据设置执行上述流程
   - 处理异常和重试逻辑

## 扩展指南

### 添加新的分析维度

要添加新的项目分析维度（例如代码行数）：

1. 在 `analyzer.py` 中添加新的检测函数：

```python
def count_code_lines(project_path: Path) -> int:
    """计算项目代码行数"""
    total_lines = 0
    # 实现计数逻辑
    return total_lines
```

2. 在 `analyze_project()` 中调用新函数：

```python
def analyze_project(project_path: Path) -> Dict[str, Any]:
    # 现有代码...
    
    # 添加新分析维度
    code_lines = count_code_lines(project_path)
    project_info['code_lines'] = code_lines
    
    return project_info
```

3. 修改 `notion_client.py` 中的 `_build_properties()` 以包含新字段：

```python
def _build_properties(self, project_info: Dict[str, Any]) -> Dict[str, Any]:
    # 现有代码...
    
    # 添加新属性
    if 'code_lines' in project_info:
        properties["代码行数"] = {
            "number": project_info["code_lines"]
        }
    
    return properties
```

### 修改 Notion 集成

要支持其他 Notion 数据结构或页面模板：

1. 修改 `NotionClient` 类中的方法
2. 调整 `_build_properties()` 函数以映射新的数据结构
3. 更新 `setup_notion_db.py` 以创建相应的数据库结构

### 实现自定义调度策略

要实现复杂的调度策略（如工作日/周末不同步率）：

1. 在 `scheduler.py` 中创建新的调度函数：

```python
def run_workday_weekend_scheduler(workday_job, weekend_job):
    """工作日/周末差异化调度"""
    # 实现调度逻辑
```

2. 在 `main.py` 中添加相应的命令行选项和处理逻辑

## API 文档

### analyzer.py

#### `get_projects(scan_dir: Path) -> List[Path]`

扫描目录并返回项目路径列表。

**参数**:
- `scan_dir`: 要扫描的目录路径

**返回值**:
- 项目路径列表

#### `analyze_project(project_path: Path) -> Dict[str, Any]`

分析单个项目并返回项目信息。

**参数**:
- `project_path`: 项目路径

**返回值**:
- 包含项目信息的字典，键包括:
  - `name`: 项目名称
  - `path`: 项目路径
  - `tech_stack`: 技术栈列表
  - `project_type`: 项目类型
  - `status`: 项目状态
  - `priority`: 项目优先级
  - `description`: 项目描述
  - `last_modified`: 最后修改日期

### notion_client.py

#### `NotionClient(api_key: str, database_id: str)`

Notion API 客户端类。

**参数**:
- `api_key`: Notion API 密钥
- `database_id`: Notion 数据库 ID

#### `NotionClient.load_existing_projects() -> Dict[str, str]`

加载已存在的项目。

**返回值**:
- 项目名称到页面 ID 的映射

#### `NotionClient.create_project(project_info: Dict[str, Any]) -> Optional[str]`

创建新项目页面。

**参数**:
- `project_info`: 项目信息字典

**返回值**:
- 创建的页面 ID，失败则返回 None

#### `NotionClient.update_project(page_id: str, project_info: Dict[str, Any]) -> bool`

更新已有项目页面。

**参数**:
- `page_id`: 页面 ID
- `project_info`: 更新后的项目信息

**返回值**:
- 是否更新成功

#### `sync_projects(projects_info: List[Dict[str, Any]]) -> Dict[str, Any]`

批量同步项目信息到 Notion。

**参数**:
- `projects_info`: 项目信息列表

**返回值**:
- 同步结果统计

## 测试策略

项目使用 `unittest` 框架进行测试，测试文件位于 `tests` 目录。

测试策略包括：

1. **单元测试**：测试各个函数的独立功能
2. **模块测试**：测试模块内部组件的交互
3. **集成测试**：测试跨模块功能，使用模拟对象替代外部依赖

关键测试文件：

- `test_analyzer.py`: 测试项目分析器
- `test_notion_client.py`: 测试 Notion 客户端（使用模拟响应）

运行测试：

```bash
python run_tests.py
```
