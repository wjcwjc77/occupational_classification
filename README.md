# 职业数据转换工具

本项目用于将Excel格式的职业数据转换为JSON树形结构，便于数据分析和应用开发。

## 项目概述

通过AI Agent等工具从原始Excel文件中提取职业代码和职业名称，并转换为结构化的JSON格式数据。

## 文件说明

- `origin_data.xlsx` - 原始职业数据文件
- `processed_data.csv` - 处理后的CSV格式数据
- `occupation_tree.json` - 最终输出的JSON树形结构数据
- `convert_to_json_tree.py` - 数据转换脚本

## 环境要求

- Python 3.x
- uv (Python包管理器)

## 安装步骤

1. **安装uv包管理器**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **安装项目依赖**
   ```bash
   uv sync
   ```

3. **激活虚拟环境**
   ```bash
   source .venv/bin/activate
   ```

## 使用方法

运行数据转换脚本：
```bash
python convert_to_json_tree.py
```

执行完成后，将在项目根目录生成 `occupation_tree.json` 文件。

