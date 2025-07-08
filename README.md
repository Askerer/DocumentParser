# Document Content Extraction Service

這是一個Python FastAPI服務，提供多種檔案格式的內容擷取功能。

## 支援的檔案格式

1. **Excel檔案** (.xlsx, .xls)
   - 擷取所有工作表內容
   - 包含欄位資訊和資料統計

2. **PowerPoint檔案** (.pptx, .ppt)
   - 擷取投影片文字內容
   - 識別圖片元素

3. **XML檔案** (.xml)
   - 擷取所有XML標籤內容
   - 自動識別並擷取base64編碼的圖片
   - 儲存圖片到本地目錄

4. **PDF檔案** (.pdf)
   - 擷取文字內容（分頁）
   - 擷取並儲存圖片

5. **文字檔案** (.txt, .md, .csv, .docx)
   - 支援多種編碼格式
   - Word文件包含段落和表格資訊

## 安裝與設定

### 1. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 2. 啟動服務

```bash
python main.py
```

服務將在 `http://localhost:8000` 啟動

## API 使用方式

### 1. 上傳檔案並擷取內容

**端點**: `POST /extract`

**請求**: 使用 `multipart/form-data` 格式上傳檔案

**範例** (使用 curl):
```bash
curl -X POST "http://localhost:8000/extract" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@your_document.xlsx"
```

**範例** (使用 Python requests):
```python
import requests

url = "http://localhost:8000/extract"
files = {"file": open("your_document.xlsx", "rb")}
response = requests.post(url, files=files)
result = response.json()
print(result)
```

### 2. 健康檢查

**端點**: `GET /health`

**回應**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 3. 服務資訊

**端點**: `GET /`

**回應**:
```json
{
  "message": "Document Content Extraction Service",
  "version": "1.0.0"
}
```

## 回應格式

### Excel檔案回應範例
```json
{
  "file_type": "excel",
  "total_sheets": 2,
  "sheet_names": ["Sheet1", "Sheet2"],
  "sheets": {
    "Sheet1": {
      "data": [{"A": "value1", "B": "value2"}],
      "columns": ["A", "B"],
      "shape": [1, 2],
      "summary": {
        "total_rows": 1,
        "total_columns": 2,
        "non_null_counts": {"A": 1, "B": 1}
      }
    }
  },
  "extraction_time": "2024-01-01T12:00:00"
}
```

### XML檔案回應範例
```json
{
  "file_type": "xml",
  "root_tag": "root",
  "text_content": [
    {
      "tag": "title",
      "path": "root/title",
      "content": "文件標題"
    }
  ],
  "images_extracted": [
    {
      "tag": "image",
      "path": "root/image",
      "image_path": "extracted_images/xml_image_20240101_120000_0.png",
      "image_size": [800, 600],
      "image_format": "PNG"
    }
  ],
  "total_elements": 1,
  "total_images": 1,
  "extraction_time": "2024-01-01T12:00:00"
}
```

## 檔案限制

- 最大檔案大小: 50MB
- 支援的檔案格式: .xlsx, .xls, .pptx, .ppt, .xml, .pdf, .txt, .md, .csv, .docx

## 目錄結構

```
DocumentParser/
├── main.py              # FastAPI主程式
├── document_parser.py   # 文件解析器
├── requirements.txt     # 依賴套件
├── README.md           # 說明文件
├── uploads/            # 上傳檔案暫存目錄
└── extracted_images/   # 擷取的圖片儲存目錄
```

## 錯誤處理

服務會回傳適當的HTTP狀態碼和錯誤訊息：

- `400 Bad Request`: 檔案格式不支援或檔案過大
- `500 Internal Server Error`: 檔案解析失敗

## 開發注意事項

1. 圖片檔案會自動儲存到 `extracted_images/` 目錄
2. 上傳的檔案會在處理完成後自動刪除
3. 支援多種文字編碼格式（UTF-8, Big5, GBK等）
4. XML檔案中的base64圖片會自動識別並擷取

## API文檔

啟動服務後，可以訪問 `http://localhost:8000/docs` 查看互動式API文檔。 