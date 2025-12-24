# OpenRareDisease - FSHD 影像 AI 辅助诊断后端

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi)](https://fastapi.tiangolo.com/)

**OpenRareDisease** 是罕见病开源社区（OpenRareDisease）的一部分，本仓库提供 **FSHD（面肩肱型肌营养不良）** 影像 AI 辅助诊断系统的后端服务。

本项目使用硅基流动（SiliconFlow）大模型进行影像分析，支持单张医疗照片上传、实时推理，并返回风险概率和诊疗建议。

**重要声明**  
本系统**仅供研究和辅助用途，不构成任何医疗诊断**。  
所有上传图片在内存中处理，**不存储原始照片**，严格保护患者隐私，符合《个人信息保护法》等相关法规。

## 功能特点

- 支持单张 JPG/PNG 图片上传（≤20MB）
- 内存处理 + base64 传输（不保存原始图片）
- 集成硅基流动 Qwen2-VL-72B-Instruct 视觉大模型
- 返回风险概率（0.0-1.0）和诊疗建议
- 匿名化保存推理结果（数据库存储 file_id、概率、建议等）
- FastAPI 提供 Swagger 文档（`/docs`）
- 隐私合规设计

## 快速启动（本地开发）

### 1. 克隆仓库
```bash
git clone https://github.com/OpenRareDisease/fshd-early-screening.git
cd fshd-early-screening
2. 创建虚拟环境
Bash
python -m venv .venv
Windows

Bash
.venv\Scripts\activate
macOS/Linux

Bash
source .venv/bin/activate
3. 安装依赖
Bash
pip install -r requirements.txt
4. 配置环境变量
复制 .env.example 为 .env
Bash
copy .env.example .env  # Windows
# 或 macOS/Linux
cp .env

5. 运行服务
Bash
uvicorn app.main:app --reload --port 8000
访问 http://127.0.0.1:8000/docs 测试 API。

6. 测试上传
打开 Swagger 界面 → /api/inference → Try it out
选择一张 JPG/PNG 图片上传
检查返回的 JSON（包含 probability 和 advice）
生产部署建议
无服务器平台：Railway.app / Render.com / Vercel（免费起步，按流量付费）
合规服务器：阿里云 ECS / 腾讯云 CVM（数据境内存储）
推荐：使用 Docker Compose + PostgreSQL（代码已支持）
项目结构
text
fshd-early-screening/
├── app/                    # 核心代码
│   ├── api/                # API 接口
│   ├── core/               # 配置
│   ├── models/             # 数据库模型
│   ├── schemas/            # Pydantic 模型
│   └── services/           # 大模型调用
├── .env.example            # 环境变量模板
├── requirements.txt        # 依赖列表
├── README.md               # 本文档
├── LICENSE                 # Apache 2.0 协议
└── Dockerfile              # 容器化部署（可选）
