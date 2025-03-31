# Notion 项目更新器 - 用户指南

本指南将帮助您了解如何安装、配置和使用 Notion 项目更新器，以便自动化项目管理工作流程。

## 目录

- [安装与设置](#安装与设置)
  - [系统要求](#系统要求)
  - [安装步骤](#安装步骤)
  - [Notion API 配置](#notion-api-配置)
  - [数据库设置](#数据库设置)
- [基本使用](#基本使用)
  - [单次同步](#单次同步)
  - [定时同步](#定时同步)
  - [查看结果](#查看结果)
- [高级功能](#高级功能)
  - [自定义项目分析](#自定义项目分析)
  - [调整扫描规则](#调整扫描规则)
  - [过滤项目](#过滤项目)
- [故障排除](#故障排除)
  - [常见问题](#常见问题)
  - [日志分析](#日志分析)
  - [错误处理](#错误处理)
- [最佳实践](#最佳实践)
  - [项目组织建议](#项目组织建议)
  - [同步策略](#同步策略)
  - [Notion 模板](#notion-模板)

## 安装与设置

### 系统要求

- Python 3.7 或更高版本
- 互联网连接（用于访问 Notion API）
- Notion 账户和 API 密钥

### 安装步骤

1. 克隆或下载仓库：

   ```bash
   git clone https://github.com/innoraorg/notion-project-updater.git
   cd notion-project-updater
   ```

2. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 检查安装：

   ```bash
   python troubleshoot.py
   ```

   这个命令会检查您的环境并确保所有必要的组件都已正确安装。

### Notion API 配置

要使用 Notion API，您需要创建一个集成并获取 API 密钥：

1. 访问 [Notion Integrations](https://www.notion.so/my-integrations) 页面
2. 点击 "New integration" 按钮
3. 填写集成名称（例如 "项目更新器"）
4. 选择适当的工作区
5. 点击 "Submit" 按钮
6. 复制生成的 Internal Integration Token

获取 API 密钥后，有两种方式配置它：

#### 方式一：使用设置向导

运行：

```bash
python setup_notion_db.py
```

此脚本将引导您完成 API 密钥设置和数据库创建过程。

#### 方式二：手动配置

1. 复制 `.env.example` 文件为 `.env`
2. 编辑 `.env` 文件，填入您的 API 密钥：

   ```
   NOTION_API_KEY=your_secret_api_key
   ```

### 数据库设置

要将项目信息同步到 Notion，您需要创建一个合适的数据库：

#### 方式一：使用设置向导（推荐）

如前所述，运行 `setup_notion_db.py` 脚本将自动创建数据库并配置所需的属性。

#### 方式二：手动创建

1. 在 Notion 中创建一个新的数据库
2. 添加以下属性：
   - 名称（标题类型）
   - 路径（文本类型）
   - 技术栈（多选类型）
   - 项目类型（单选类型）
   - 状态（单选类型，选项：活跃、维护中、暂停）
   - 优先级（单选类型，选项：高、中、低）
   - 描述（文本类型）
   - 最后修改日期（日期类型）
3. 获取数据库 ID（从 URL 中提取）
4. 将数据库 ID 添加到 `.env` 文件：

   ```
   NOTION_DATABASE_ID=your_database_id
   ```

5. 确保您的集成有权访问此数据库：
   - 在数据库页面点击右上角的 ⋮ 菜单
   - 选择 "Connections"
   - 添加您之前创建的集成

## 基本使用

### 单次同步

要执行一次项目扫描和同步，只需运行：

```bash
python main.py
```

这将扫描配置的目录（默认为 `/Users/anwu/Documents/code`），分析所有项目，并将结果同步到 Notion 数据库。

### 定时同步

对于自动化同步，可以使用以下选项：

```bash
# 每 24 小时执行一次
python main.py --schedule

# 自定义执行间隔（例如每 12 小时）
python main.py --schedule --interval 12

# 在每天特定时间执行
python main.py --schedule --time 01:30

# 使用 cron 表达式设置执行计划
python main.py --schedule --cron "0 1 * * *"
```

**注意**：定时执行模式下，程序会持续运行。如果您想在后台运行，可以使用 `nohup` 或系统服务。

### 查看结果

同步完成后，您可以在 Notion 数据库中查看结果。每个项目将作为一个页面，包含以下信息：

- 项目名称
- 项目路径
- 检测到的技术栈
- 项目类型
- 项目状态
- 优先级
- 项目描述
- 最后修改日期

## 高级功能

### 自定义项目分析

如果您想自定义项目分析逻辑，可以修改 `analyzer.py` 文件或创建自己的分析器。以下是一个自定义分析器的示例：

```python
# custom_analyzer.py
from analyzer import analyze_project

def my_custom_analyzer(project_path):
    # 获取基本分析结果
    project_info = analyze_project(project_path)
    
    # 添加自定义信息
    project_info['custom_field'] = "自定义值"
    
    return project_info
```

查看 `examples/custom_analyzer.py` 获取更详细的示例。

### 调整扫描规则

您可以通过编辑 `config.py` 文件来调整扫描规则：

```python
# 修改扫描目录
SCAN_DIR = Path("/path/to/your/projects")

# 自定义技术栈检测规则
TECH_STACK_MARKERS = {
    "Your Tech": ["marker1", "marker2"],
    # ...
}

# 自定义项目类型检测规则
PROJECT_TYPE_MARKERS = {
    "Your Type": ["marker1", "marker2"],
    # ...
}

# 修改活跃项目阈值
GIT_ACTIVE_THRESHOLD_DAYS = 15  # 15天内有提交视为活跃项目
```

### 过滤项目

如果您想排除某些项目或只同步特定项目，可以修改 `get_projects` 函数：

```python
def get_projects(scan_dir: Path) -> List[Path]:
    # 原始扫描逻辑
    projects = [
        item for item in scan_dir.iterdir() 
        if item.is_dir() and not item.name.startswith('.')
    ]
    
    # 添加过滤条件
    filtered_projects = [
        p for p in projects 
        if not p.name.startswith('temp_') and not p.name.endswith('_old')
    ]
    
    return filtered_projects
```

## 故障排除

### 常见问题

#### 问题：找不到任何项目

- 检查 `config.py` 中的 `SCAN_DIR` 设置
- 确保扫描目录包含有效的项目文件夹
- 检查是否有权限访问扫描目录

#### 问题：Notion API 认证失败

- 确认 `.env` 文件中的 API 密钥是正确的
- 检查网络连接
- 验证 API 密钥是否过期或被撤销

#### 问题：项目分析失败

- 检查项目结构是否异常
- 查看日志文件获取详细错误信息
- 确保有足够的权限读取项目文件

### 日志分析

项目日志存储在 `logs/app.log` 文件中。常见的日志级别包括：

- `INFO`: 普通操作信息
- `WARNING`: 潜在问题警告
- `ERROR`: 操作失败
- `DEBUG`: 详细调试信息

### 错误处理

如果您遇到问题，可以运行故障排除工具：

```bash
python troubleshoot.py
```

此工具将检查常见问题并提供解决方案。

## 最佳实践

### 项目组织建议

为了获得最佳分析结果，建议：

- 为每个项目创建一个清晰的 README.md 文件
- 使用 Git 进行版本控制
- 保持项目结构一致
- 避免在一个目录中嵌套多个项目

### 同步策略

根据项目规模和更新频率，选择适当的同步策略：

- **小型个人项目**：每天同步一次足够
- **活跃开发团队**：考虑每 6-12 小时同步一次
- **大型企业**：可能需要更复杂的策略，如工作时间每小时同步

### Notion 模板

您可以基于同步的数据创建多种 Notion 视图：

- **看板视图**：按项目状态分组
- **表格视图**：显示所有项目详情
- **日历视图**：基于最后修改日期
- **画廊视图**：为每个项目添加封面图片

这些视图可以帮助您以不同方式可视化和管理项目信息。
