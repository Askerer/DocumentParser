# 文件內容擷取服務測試框架

這是一個完整的測試框架，用於測試文件內容擷取服務的各種功能。支援多種檔案格式和測試模式。

## 🌟 功能特色

- **完整的測試覆蓋**：單元測試、整合測試、效能測試
- **多檔案格式支援**：Excel、PowerPoint、XML、PDF、Word、文字檔案
- **自動測試檔案生成**：自動建立各種格式的測試檔案
- **效能分析**：測量處理時間和吞吐量
- **自定義檔案測試**：可以測試你自己的檔案
- **詳細報告**：生成JSON格式的測試報告

## 📁 專案結構

```
.
├── tests/                      # 測試檔案目錄
│   ├── __init__.py
│   ├── test_document_parser.py # DocumentParser 單元測試
│   └── test_api.py            # FastAPI 整合測試
├── test_runner.py             # 主要測試運行器
├── setup_and_run_tests.py     # 一鍵安裝和測試腳本
├── pytest.ini                # pytest 配置檔案
├── requirements.txt           # 依賴清單（已更新包含測試工具）
└── README_測試說明.md         # 本說明檔案
```

## 🚀 快速開始

### 方法一：一鍵安裝和測試（推薦）

```bash
python setup_and_run_tests.py
```

這個腳本會自動：
1. 安裝所有必要的依賴
2. 建立範例測試檔案
3. 運行快速測試
4. 顯示更多測試選項

### 方法二：手動安裝

1. **安裝依賴**
```bash
pip install -r requirements.txt
```

2. **運行測試**
```bash
# 運行所有測試
python test_runner.py --mode all

# 運行特定類型的測試
python test_runner.py --mode unit          # 單元測試
python test_runner.py --mode integration   # 整合測試
python test_runner.py --mode performance   # 效能測試
```

## 📖 測試模式說明

### 1. 單元測試 (`--mode unit`)

測試 `DocumentParser` 類別的各個方法：

- Excel 檔案內容擷取
- PowerPoint 檔案內容擷取
- XML 檔案內容擷取
- Word 檔案內容擷取
- 文字檔案內容擷取
- 編碼檢測
- Base64 圖片檢測
- 錯誤處理

```bash
python test_runner.py --mode unit
```

### 2. 整合測試 (`--mode integration`)

測試 FastAPI 應用程式的端點：

- 根端點 (`/`)
- 健康檢查端點 (`/health`)
- 檔案擷取端點 (`/extract`)
- 各種檔案格式的上傳和處理
- 錯誤情況處理

```bash
python test_runner.py --mode integration
```

### 3. 效能測試 (`--mode performance`)

測試不同檔案大小和格式的處理效能：

- 小型 Excel 檔案
- 大型 Excel 檔案
- 文字檔案
- PowerPoint 檔案
- XML 檔案
- Word 檔案

測量指標：
- 檔案大小（MB）
- 處理時間（秒）
- 吞吐量（MB/秒）

```bash
python test_runner.py --mode performance
```

### 4. 自定義檔案測試 (`--mode custom`)

測試你自己的檔案：

```bash
# 測試單個檔案
python test_runner.py --mode custom --files your_file.xlsx

# 測試多個檔案
python test_runner.py --mode custom --files file1.xlsx file2.pdf file3.txt

# 測試整個目錄的檔案
python test_runner.py --mode custom --files path/to/files/*
```

## 📊 測試報告

### 輸出報告到檔案

```bash
python test_runner.py --mode all --output test_report.json
```

報告包含：
- 測試狀態（成功/失敗/錯誤）
- 詳細錯誤訊息
- 效能指標
- 處理結果摘要

### 報告格式範例

```json
{
  "unit_tests": {
    "status": "success",
    "returncode": 0,
    "stdout": "測試輸出...",
    "stderr": "",
    "duration": 0
  },
  "performance_tests": {
    "status": "completed",
    "results": {
      "small_excel": {
        "file_size_bytes": 5234,
        "file_size_mb": 0.005,
        "processing_time_seconds": 0.123,
        "throughput_mb_per_second": 0.04,
        "status": "success"
      }
    }
  }
}
```

## 🛠️ 進階使用

### 使用 pytest 直接運行

```bash
# 運行所有測試
pytest

# 運行特定測試檔案
pytest tests/test_document_parser.py

# 運行特定測試方法
pytest tests/test_document_parser.py::TestDocumentParser::test_extract_excel_content

# 顯示詳細輸出
pytest -v

# 顯示測試覆蓋率
pytest --cov=document_parser
```

### 建立自己的測試檔案

在 `tests/` 目錄下建立新的測試檔案：

```python
import pytest
from document_parser import DocumentParser

class TestMyCustomFeature:
    @pytest.fixture
    def parser(self):
        return DocumentParser()
    
    def test_my_feature(self, parser):
        # 你的測試邏輯
        assert True
```

## 📋 支援的檔案格式

| 格式 | 副檔名 | 測試內容 |
|------|--------|----------|
| Excel | .xlsx, .xls | 工作表、數據、欄位 |
| PowerPoint | .pptx, .ppt | 投影片、文字內容 |
| XML | .xml | 元素、屬性、圖片 |
| PDF | .pdf | 文字、圖片（透過 PyMuPDF） |
| Word | .docx | 段落、表格 |
| 文字檔案 | .txt, .md, .csv | 內容、編碼檢測 |

## 🔧 故障排除

### 常見問題

1. **依賴安裝失敗**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **測試檔案無法建立**
   - 檢查寫入權限
   - 確保有足夠的磁碟空間

3. **模組導入錯誤**
   - 確保在專案根目錄執行
   - 檢查 Python 路徑設定

4. **效能測試結果異常**
   - 第一次運行可能較慢（模組載入）
   - 確保系統資源充足

### 偵錯模式

```bash
# 顯示詳細錯誤訊息
python test_runner.py --mode unit 2>&1 | tee test_debug.log

# 使用 pytest 的偵錯選項
pytest -v --tb=long --capture=no
```

## 🤝 貢獻

要添加新的測試：

1. 在 `tests/` 目錄下建立測試檔案
2. 遵循 pytest 命名慣例（以 `test_` 開頭）
3. 使用清楚的測試方法名稱
4. 添加適當的文檔字串

## 📄 授權

本測試框架遵循與主專案相同的授權條款。

---

**注意**：第一次運行可能需要較長時間來安裝依賴和建立測試檔案。後續運行會更快速。