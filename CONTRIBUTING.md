# 贡献指南

首先，感谢你考虑为 Notion 项目更新器做出贡献！我们欢迎任何形式的贡献，包括但不限于：

- 代码改进
- 文档完善
- Bug 报告
- 功能建议
- 测试案例

## 目录

- [行为准则](#行为准则)
- [如何贡献](#如何贡献)
  - [报告 Bug](#报告-bug)
  - [提交功能请求](#提交功能请求)
  - [代码贡献](#代码贡献)
- [开发环境设置](#开发环境设置)
- [代码风格](#代码风格)
- [测试](#测试)
- [提交指南](#提交指南)
- [分支策略](#分支策略)
- [发布流程](#发布流程)

## 行为准则

这个项目期望所有参与者遵守友好、尊重的交流原则。我们希望创建一个积极和包容的环境，鼓励开放式协作。

## 如何贡献

### 报告 Bug

如果你发现了 Bug，请通过 GitHub Issues 报告。创建 Bug 报告时，请确保包含：

1. 问题的清晰描述
2. 重现步骤
3. 预期行为与实际行为
4. 环境信息（操作系统、Python 版本等）
5. 如可能，提供日志或截图

### 提交功能请求

我们欢迎新功能的建议。要提交功能请求：

1. 在 GitHub Issues 中创建新的 Issue
2. 使用标题清晰描述建议的功能
3. 详细说明此功能如何工作以及为何有用
4. 如可能，提供示例或草图

### 代码贡献

如果你想贡献代码：

1. Fork 仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 开发环境设置

要设置开发环境：

1. 克隆仓库：
   ```bash
   git clone https://github.com/yourusername/notion-project-updater.git
   cd notion-project-updater
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # 在 Windows 上使用 venv\Scripts\activate
   ```

3. 安装开发依赖：
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # 如果存在
   ```

4. 配置开发环境：
   ```bash
   cp .env.example .env
   # 编辑 .env 文件添加你的测试凭据
   ```

## 代码风格

我们使用 PEP 8 作为 Python 代码风格指南。请确保你的代码符合以下要求：

- 使用 4 个空格进行缩进（不使用制表符）
- 行长度限制为 100 字符
- 使用有意义的变量名和函数名
- 为类、方法和函数添加文档字符串

建议使用 `flake8` 和 `black` 检查和格式化你的代码：

```bash
# 检查代码风格
flake8 .

# 格式化代码
black .
```

## 测试

我们使用 `unittest` 进行测试。在提交 Pull Request 之前，请确保所有测试都能通过：

```bash
# 运行所有测试
python run_tests.py
```

如果你添加了新功能，请同时添加相应的测试用例。测试文件应放在 `tests` 目录中，并以 `test_` 开头。

## 提交指南

提交消息应清晰描述更改内容，包括以下方面：

- 使用现在时态（"Add feature"，而不是"Added feature"）
- 第一行是简短摘要（50 字符以内）
- 如果需要，可以添加详细说明，与摘要之间空一行
- 参考相关 issue 编号（如适用）

例如：

```
Add automatic detection of project language

This commit adds functionality to automatically detect
the primary programming language used in a project
based on file extensions and directory structure.

Fixes #42
```

## 分支策略

- `main`: 主分支，包含稳定版本的代码
- `develop`: 开发分支，包含下一版本的功能
- `feature/*`: 特性分支，用于开发新功能
- `bugfix/*`: 修复分支，用于修复 Bug
- `release/*`: 发布分支，用于发布准备

所有开发工作应在特性分支或修复分支中进行，然后通过 Pull Request 合并到 `develop` 分支。

## 发布流程

1. 从 `develop` 分支创建发布分支 (`release/vX.Y.Z`)
2. 在发布分支上进行最终测试和调整
3. 将发布分支合并到 `main` 分支
4. 在 `main` 分支上创建标签 (`vX.Y.Z`)
5. 将 `main` 分支的更改合并回 `develop` 分支

---

再次感谢你的贡献！如有任何问题，请随时联系维护者。
