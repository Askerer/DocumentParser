#!/usr/bin/env python3
"""
簡單的測試示範程式

這個腳本展示如何測試不同的檔案，不需要完整的測試環境設置。
它可以直接測試現有的檔案或建立簡單的測試檔案。
"""

import os
import sys
import tempfile
import time
import json
from pathlib import Path
from datetime import datetime

# 添加當前目錄到Python路徑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_simple_test_files():
    """建立簡單的測試檔案"""
    print("📁 建立簡單測試檔案...")
    
    test_files_dir = Path("demo_test_files")
    test_files_dir.mkdir(exist_ok=True)
    
    created_files = []
    
    # 建立文字檔案
    txt_path = test_files_dir / "demo.txt"
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write("""示範文字檔案

這是一個用於測試的示範檔案。

內容包括：
1. 中文字符測試
2. 多行文字內容
3. 特殊字符：@#$%^&*()

測試目的：
- 驗證文字檔案讀取功能
- 測試UTF-8編碼支援
- 檢查多行文字處理

結束。""")
    created_files.append(str(txt_path))
    
    # 建立XML檔案
    xml_path = test_files_dir / "demo.xml"
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<產品目錄>
    <產品 id="1">
        <名稱>筆記型電腦</名稱>
        <價格>25000</價格>
        <規格>
            <處理器>Intel i7</處理器>
            <記憶體>16GB</記憶體>
            <硬碟>512GB SSD</硬碟>
        </規格>
        <描述>高效能筆記型電腦，適合工作和娛樂</描述>
    </產品>
    <產品 id="2">
        <名稱>智慧手機</名稱>
        <價格>15000</價格>
        <規格>
            <螢幕>6.1吋 OLED</螢幕>
            <相機>48MP 三鏡頭</相機>
            <電池>4000mAh</電池>
        </規格>
        <描述>功能強大的智慧手機</描述>
    </產品>
</產品目錄>"""
    
    with open(xml_path, 'w', encoding='utf-8') as f:
        f.write(xml_content)
    created_files.append(str(xml_path))
    
    # 建立CSV檔案
    csv_path = test_files_dir / "demo.csv"
    csv_content = """姓名,部門,職位,薪資,入職日期
張三,工程部,軟體工程師,60000,2023-01-15
李四,市場部,市場專員,45000,2023-02-20
王五,人資部,人資主管,55000,2022-11-10
趙六,財務部,會計師,50000,2023-03-01
陳七,工程部,資深工程師,75000,2022-08-15"""
    
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write(csv_content)
    created_files.append(str(csv_path))
    
    print(f"✅ 已建立 {len(created_files)} 個示範檔案:")
    for file_path in created_files:
        file_size = os.path.getsize(file_path)
        print(f"  - {file_path} ({file_size} bytes)")
    
    return created_files

def test_document_parser_basic(file_paths):
    """基本的文件解析測試"""
    print("\n🧪 開始基本文件解析測試...")
    
    try:
        from document_parser import DocumentParser
        parser = DocumentParser()
        print("✅ DocumentParser 載入成功")
    except ImportError as e:
        print(f"❌ 無法載入 DocumentParser: {e}")
        return False
    except Exception as e:
        print(f"❌ DocumentParser 初始化失敗: {e}")
        return False
    
    test_results = {}
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            print(f"⚠️  檔案不存在: {file_path}")
            continue
        
        file_name = os.path.basename(file_path)
        file_extension = Path(file_path).suffix.lower()
        file_size = os.path.getsize(file_path)
        
        print(f"\n📄 測試檔案: {file_name}")
        print(f"   格式: {file_extension}")
        print(f"   大小: {file_size} bytes")
        
        try:
            start_time = time.time()
            result = parser.extract_content(file_path, file_extension)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            print(f"✅ 解析成功 (耗時: {processing_time:.3f}秒)")
            
            # 顯示解析結果摘要
            if result.get('file_type') == 'txt':
                print(f"   內容長度: {len(result.get('content', ''))} 字符")
                print(f"   行數: {result.get('total_lines', 0)}")
                print(f"   編碼: {result.get('encoding', 'unknown')}")
            elif result.get('file_type') == 'xml':
                print(f"   根元素: {result.get('root_tag', 'unknown')}")
                print(f"   元素數量: {result.get('total_elements', 0)}")
                print(f"   圖片數量: {result.get('total_images', 0)}")
            elif result.get('file_type') == 'csv':
                print(f"   內容長度: {len(result.get('content', ''))} 字符")
                print(f"   行數: {result.get('total_lines', 0)}")
            
            # 顯示部分內容（前100字符）
            content_preview = ""
            if 'content' in result:
                content_preview = result['content'][:100]
            elif 'text_content' in result and result['text_content']:
                content_preview = str(result['text_content'][:2])[:100]
            
            if content_preview:
                print(f"   內容預覽: {content_preview}...")
            
            test_results[file_name] = {
                "status": "success",
                "file_size": file_size,
                "processing_time": round(processing_time, 3),
                "file_type": result.get('file_type', 'unknown')
            }
            
        except Exception as e:
            print(f"❌ 解析失敗: {str(e)}")
            test_results[file_name] = {
                "status": "error",
                "error": str(e),
                "file_size": file_size
            }
    
    return test_results

def test_existing_files():
    """測試現有的檔案"""
    print("\n🔍 搜尋現有測試檔案...")
    
    existing_files = []
    
    # 搜尋各種可能的測試檔案
    search_patterns = [
        "test_files/*.txt",
        "test_files/*.xml", 
        "test_files/*.csv",
        "sample_test_files/*.txt",
        "sample_test_files/*.xml",
        "sample_test_files/*.csv",
        "demo_test_files/*.txt",
        "demo_test_files/*.xml",
        "demo_test_files/*.csv",
        "*.txt",
        "*.xml",
        "*.csv"
    ]
    
    import glob
    for pattern in search_patterns:
        files = glob.glob(pattern)
        for file in files:
            if os.path.isfile(file) and file not in existing_files:
                existing_files.append(file)
    
    # 限制檔案數量，避免測試過多檔案
    existing_files = existing_files[:10]
    
    if existing_files:
        print(f"找到 {len(existing_files)} 個現有檔案:")
        for file in existing_files:
            size = os.path.getsize(file)
            print(f"  - {file} ({size} bytes)")
        return existing_files
    else:
        print("未找到現有測試檔案")
        return []

def generate_simple_report(results):
    """生成簡單的測試報告"""
    print("\n" + "="*60)
    print("📊 測試結果摘要")
    print("="*60)
    
    if not results:
        print("沒有測試結果")
        return
    
    total_tests = len(results)
    successful_tests = sum(1 for r in results.values() if r.get('status') == 'success')
    failed_tests = total_tests - successful_tests
    
    print(f"總測試數: {total_tests}")
    print(f"成功: {successful_tests}")
    print(f"失敗: {failed_tests}")
    print(f"成功率: {(successful_tests/total_tests)*100:.1f}%")
    
    print("\n詳細結果:")
    for file_name, result in results.items():
        status_icon = "✅" if result.get('status') == 'success' else "❌"
        print(f"{status_icon} {file_name}")
        
        if result.get('status') == 'success':
            print(f"    檔案大小: {result.get('file_size', 0)} bytes")
            print(f"    處理時間: {result.get('processing_time', 0)} 秒")
            print(f"    檔案類型: {result.get('file_type', 'unknown')}")
        else:
            print(f"    錯誤: {result.get('error', 'unknown error')}")
    
    # 儲存JSON報告
    report_file = f"demo_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": {
                    "total_tests": total_tests,
                    "successful_tests": successful_tests,
                    "failed_tests": failed_tests,
                    "success_rate": round((successful_tests/total_tests)*100, 1)
                },
                "results": results,
                "timestamp": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        print(f"\n📋 詳細報告已儲存至: {report_file}")
    except Exception as e:
        print(f"⚠️  無法儲存報告: {e}")

def main():
    """主程式"""
    print("🎯 文件內容擷取服務 - 簡單測試示範")
    print("="*50)
    
    # 1. 測試現有檔案
    existing_files = test_existing_files()
    
    # 2. 建立示範檔案
    demo_files = create_simple_test_files()
    
    # 3. 合併檔案列表
    all_files = existing_files + demo_files
    
    if not all_files:
        print("❌ 沒有檔案可以測試")
        return
    
    # 4. 運行測試
    test_results = test_document_parser_basic(all_files)
    
    # 5. 生成報告
    if test_results:
        generate_simple_report(test_results)
    
    print("\n🎉 測試示範完成！")
    print("\n💡 要運行完整的測試套件，請使用：")
    print("   python setup_and_run_tests.py")
    print("   python test_runner.py --mode all")

if __name__ == "__main__":
    main()