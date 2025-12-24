# app/api/inference.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from uuid import uuid4
import base64
import os
from ..core.config import settings
from ..services.vision_client import VisionModelClient
from ..models.database import InferenceRecord, Base
from ..schemas.response import InferenceResponse

router = APIRouter(prefix="/api")

# 数据库依赖（每次请求时动态创建 engine 和 session）
def get_db():
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 启动时创建表
def init_db():
    engine = create_engine(settings.DATABASE_URL)
    Base.metadata.create_all(bind=engine)

@router.post("/inference", response_model=InferenceResponse)
async def inference(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. 文件校验
    allowed_ext = {".jpg", ".jpeg", ".png"}
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in allowed_ext:
        raise HTTPException(400, "仅支持 JPG/PNG 格式")
    if file.size > 20 * 1024 * 1024:
        raise HTTPException(413, "文件大小超过 20MB")

    # 2. 内存中读取文件内容
    file_content = await file.read()  # 一次性读取到内存
    img_base64 = base64.b64encode(file_content).decode("utf-8")

    # 3. 调用大模型（使用 base64）
    client = VisionModelClient()
    try:
        result = client.infer_from_base64(img_base64)
    except Exception as e:
        raise HTTPException(500, f"模型调用失败: {str(e)}")

    # 4. 生成唯一ID（用于审计）
    file_id = str(uuid4())

    # 5. 保存记录到数据库（不存原始图片，只存结果和元数据）
    record = InferenceRecord(
        file_id=file_id,
        original_filename=file.filename,
        risk_probability=result.risk_probability,
        advice=result.advice,
        raw_response=result.dict(),
        image_url=None  # 不返回图片URL
    )
    db.add(record)
    db.commit()

    # 6. 显式释放内存
    file_content = None

    # 7. 返回结果（隐私声明）
    privacy_notice = "（AI辅助分析，仅供参考，不构成医疗诊断。本系统不存储您的原始照片）"
    full_advice = f"{result.advice} {privacy_notice}"

    response_data = InferenceResponse(
        status="success",
        probability=result.risk_probability,
        advice=full_advice,
        image_url=None
    )

    return response_data