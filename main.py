from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from document_parser import DocumentParser
import os
from datetime import datetime

app = FastAPI(
    title="Document Content Extraction Service",
    description="A service for extracting content from various document formats",
    version="1.0.0"
)

# 建立上傳目錄
UPLOAD_DIR = "uploads"
IMAGES_DIR = "extracted_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

document_parser = DocumentParser()

@app.get("/")
async def root():
    return {"message": "Document Content Extraction Service", "version": "1.0.0"}

@app.post("/extract")
async def extract_document_content(file: UploadFile = File(...)):
    """
    上傳檔案並擷取內容
    支援的格式：Excel (.xlsx, .xls), PowerPoint (.pptx, .ppt), XML, PDF, 文字檔案 (.txt, .md, .csv)
    """
    try:
        # 檢查檔案大小 (限制為50MB)
        if file.size and file.size > 50 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="檔案大小不能超過50MB")
        
        # 檢查檔案類型
        allowed_extensions = {
            '.xlsx', '.xls', '.pptx', '.ppt', '.xml', '.pdf', 
            '.txt', '.md', '.csv', '.docx'
        }
        
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"不支援的檔案格式: {file_extension}. 支援的格式: {', '.join(allowed_extensions)}"
            )
        
        # 儲存上傳的檔案
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename.replace(' ', '_')}"
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 根據檔案類型擷取內容
        result = document_parser.extract_content(file_path, file_extension)
        
        # 清理上傳的檔案
        os.remove(file_path)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        # 清理檔案（如果存在）
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"處理檔案時發生錯誤: {str(e)}")

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 