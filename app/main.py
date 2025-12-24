# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api.inference import router as inference_router, init_db  # 新增导入 init_db

app = FastAPI(title="FSHD 图像识别工具 - 后端")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(inference_router)

# 启动时创建表（只执行一次）
@app.on_event("startup")
def startup_event():
    init_db()  # 创建所有表