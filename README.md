# Notion 项目更新器 (Notion Project Updater)

<p align="center">
  <img src="https://github.com/innoraorg/notion-project-updater/raw/main/docs/images/logo.png" alt="Notion 项目更新器" width="180"/>
</p>

<p align="center">
  <b>自动扫描代码项目并同步到 Notion 数据库的 Python 工具</b><br/>
  <i>由 <a href="https://innora.ai">Innora</a> 开发</i>
</p>

<p align="center">
  <a href="#功能特点">功能特点</a> • 
  <a href="#安装">安装</a> • 
  <a href="#使用方法">使用方法</a> • 
  <a href="#项目信息分析">项目信息分析</a> • 
  <a href="#示例">示例</a> • 
  <a href="#配置选项">配置选项</a> • 
  <a href="#故障排除">故障排除</a> • 
  <a href="#关于innora">关于Innora</a>
</p>

---

## 功能特点

Notion 项目更新器是一个强大的自动化工具，能够：

- **自动扫描** - 扫描指定目录下的所有代码项目
- **智能分析** - 自动检测每个项目的技术栈、类型、状态等信息
- **Notion 集成** - 无缝将项目信息同步到 Notion 数据库
- **定时执行** - 支持多种定时执行方式，保持项目信息实时更新
- **友好界面** - 美观的命令行界面，提供直观的操作反馈
- **详细日志** - 完整的日志记录，方便故障排查

## 安装

### 前提条件

- Python 3.7 或更高版本
- Notion API 密钥（从 [Notion Integrations](https://www.notion.so/my-integrations) 获取）
- Notion 数据库 ID

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/innoraorg/notion-project-updater.git
   cd notion-project-updater
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 设置 Notion 数据库：
   ```bash
   python setup_notion_db.py
   ```

   此脚本将引导你设置 Notion API 密钥并创建必要的数据库结构。

## 使用方法

### 基本用法

```bash
# 扫描项目并同步到 Notion
python main.py
```

### 定时执行

```bash
# 每24小时执行一次
python main.py --schedule

# 自定义执行间隔（每12小时）
python main.py --schedule --interval 12

# 在每天特定时间执行
python main.py --schedule --time 01:30

# 使用cron表达式设置执行计划
python main.py --schedule --cron "0 1 * * *"
```

## 项目信息分析

Notion 项目更新器可以自动分析以下项目信息：

| 信息类型 | 描述 | 检测方法 |
| ------- | ---- | ------- |
| 项目名称 | 项目的名称 | 从文件夹名称获取 |
| 项目路径 | 项目的完整路径 | 从文件系统获取 |
| 技术栈 | 项目使用的编程语言和框架 | 基于文件扩展名和特定标记文件 |
| 项目类型 | 项目类别（Web应用、CLI工具等） | 基于目录结构和技术栈 |
| 项目状态 | 开发状态（活跃、维护中、暂停） | 基于Git提交历史或文件修改时间 |
| 项目优先级 | 项目的优先级（高、中、低） | 基于状态和最后修改时间 |
| 项目描述 | 项目的简要描述 | 从README文件中提取 |
| 最后修改日期 | 项目的最后更新时间 | 从Git历史或文件修改时间获取 |

## 示例

### 快速开始示例

```bash
python examples/quick_start.py
```

此示例将扫描配置的目录，分析前几个项目，并询问是否同步到Notion。

### 自定义分析器示例

```bash
python examples/custom_analyzer.py
```

此示例展示如何创建和使用自定义项目分析器。

### 定时同步示例

```bash
python examples/scheduled_sync.py
```

此示例演示如何设置定时同步任务。

## 配置选项

### 基本配置

编辑 `.env` 文件设置 Notion API 凭证：

```
NOTION_API_KEY=your_secret_api_key
NOTION_DATABASE_ID=your_database_id
```

### 高级配置

编辑 `config.py` 文件自定义分析规则：

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
```

## 故障排除

如果你遇到问题，可以运行故障排除工具：

```bash
python troubleshoot.py
```

此工具将检查常见问题并提供解决方案。

## 关于Innora

<p align="center">
  <img src="https://innora.ai/assets/images/innora-logo.png" alt="Innora Logo" width="200"/>
</p>

[Innora](https://innora.ai) 是一家专注于人工智能和自动化领域的创新型科技公司。我们致力于开发智能工具和解决方案，帮助个人和企业提高工作效率，简化复杂流程。

Innora 提供：

- **AI驱动的自动化工具** - 简化重复性任务
- **智能数据分析解决方案** - 从数据中获取洞察
- **定制化开发服务** - 满足特定业务需求

通过 Notion 项目更新器，我们希望帮助开发者和团队更有效地管理和跟踪他们的代码项目。

## 许可证

[MIT](LICENSE)
