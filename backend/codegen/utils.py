import re


def extract_html_content(text: str) -> str:
    text = text.strip("```")
    text = text.strip()
    # Regex to match <!DOCTYPE ...> optionally, followed by <html ...> ... </html>
    pattern = re.compile(
        r"(<!DOCTYPE[^>]*>\s*)?(<html[^>]*>.*?</html>)",
        re.DOTALL | re.IGNORECASE
    )
    match = pattern.search(text)
    if match:
        # Return the full match (doctype + html)
        return (match.group(1) or "") + match.group(2)
    else:
        # If no html tags found, print warning and return the original text
        print("[HTML Extraction] No <html> tags found in the generated content:")
        print(text)
        return text

if __name__ == "__main__":
    # Example usage
    sample_text = """
```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>請求書発行</title>
    <style>
        body {
            font-family: 'MS UI Gothic', 'Meiryo', sans-serif;
            background-color: #E0F0E0;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
            padding: 20px;
            box-sizing: border-box;
        }

        .container {
            width: 1100px;
            background-color: #E0F0E0;
            border: 1px solid #A0A0A0;
            box-shadow: 0 0 5px rgba(0,0,0,0.1);
            padding: 10px;
            box-sizing: border-box;
        }

        .dark-green-bg {
            background-color: #006633;
            color: white;
            padding: 4px 8px;
            border: 1px solid #004422;
            display: flex;
            align-items: center;
            white-space: nowrap;
            box-sizing: border-box;
        }

        .input-field {
            border: 1px solid #808080;
            padding: 3px 5px;
            background-color: white;
            font-size: 14px;
            box-sizing: border-box;
            height: 24px;
        }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }

        .header-left {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
        }

        .header-left .label-gray {
            color: #808080;
            font-size: 12px;
            margin-bottom: 2px;
        }

        .header-left .title {
            font-size: 20px;
            font-weight: bold;
            padding: 5px 15px;
            border: 1px solid #004422;
        }

        .header-right {
            display: grid;
            grid-template-columns: auto auto auto auto auto auto;
            gap: 5px;
            align-items: center;
            font-size: 14px;
        }

        .header-right .header-item {
            display: flex;
            align-items: center;
        }

        .header-right .header-item .label {
            padding: 4px 8px;
            border: 1px solid #004422;
            background-color: #006633;
            color: white;
            white-space: nowrap;
        }

        .header-right .header-item input[type="text"] {
            width: 80px;
            margin-left: 5px;
        }
        .header-right .header-item input[type="checkbox"] {
            margin-left: 5px;
            width: 16px;
            height: 16px;
        }
        .header-right .header-item .date-input {
            width: 120px;
            margin-left: 5px;
        }
        .header-right .header-item .date-separator {
            margin: 0 5px;
        }
        .header-right .header-item .count-display {
            width: 40px;
            text-align: right;
            padding-right: 5px;
        }

        .main-content {
            display: flex;
            gap: 10px;
            margin-bottom: 10px;
        }

        .input-panel {
            flex: 0 0 500px;
            display: flex;
            flex-direction: column;
            gap: 5px;
            padding-right: 10px;
        }

        .input-row {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 14px;
        }

        .input-row .label {
            width: 120px;
            text-align: right;
            padding: 4px 8px;
            border: 1px solid #004422;
            background-color: #006633;
            color: white;
            white-space: nowrap;
            box-sizing: border-box;
        }

        .input-row .input-group {
            display: flex;
            align-items: center;
            flex-grow: 1;
            gap: 5px;
        }

        .input-row .input-group input[type="text"] {
            width: 30px;
            text-align: center;
        }

        .input-row .input-group .radio-group {
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }

        .input-row .input-group .radio-option {
            display: flex;
            align-items: center;
            white-space: nowrap;
        }

        .input-row .input-group .radio-option input[type="radio"] {
            margin-right: 3px;
            width: 16px;
            height: 16px;
        }

        .input-row .input-group .text-input-full {
            flex-grow: 1;
            width: auto;
        }

        .input-row .input-group .search-input-wrapper {
            display: flex;
            align-items: center;
            border: 1px solid #808080;
            background-color: white;
            height: 24px;
            flex-grow: 1;
        }

        .input-row .input-group .search-input-wrapper input {
            border: none;
            outline: none;
            padding: 3px 5px;
            flex-grow: 1;
            height: 100%;
            box-sizing: border-box;
        }

        .input-row .input-group .search-icon {
            width: 24px;
            height: 24px;
            background-color: #E0E0E0;
            border-left: 1px solid #808080;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 16px;
            color: #555;
            cursor: pointer;
        }

        .input-row .input-group select {
            border: 1px solid #808080;
            padding: 3px 5px;
            background-color: white;
            font-size: 14px;
            height: 24px;
            box-sizing: border-box;
        }

        .table-panel {
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            border: 1px solid #808080;
            background-color: #C0C0C0;
            overflow: hidden;
        }

        .table-panel table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }

        .table-panel thead th {
            background-color: #006633;
            color: white;
            padding: 5px 8px;
            border: 1px solid #004422;
            text-align: center;
            font-weight: normal;
            white-space: nowrap;
            box-sizing: border-box;
        }

        .table-panel tbody {
            display: block;
            height: 300px;
            overflow-y: scroll;
            overflow-x: scroll;
            background-color: #C0C0C0;
        }

        .table-panel tbody tr {
            display: table;
            width: 100%;
            table-layout: fixed;
        }

        .table-panel tbody td {
            padding: 5px 8px;
            border: 1px solid #D0D0D0;
            text-align: left;
            white-space: nowrap;
            box-sizing: border-box;
            height: 28px;
        }

        .table-panel thead th:nth-child(1), .table-panel tbody td:nth-child(1) { width: 60px; }
        .table-panel thead th:nth-child(2), .table-panel tbody td:nth-child(2) { width: 100px; }
        .table-panel thead th:nth-child(3), .table-panel tbody td:nth-child(3) { width: 100px; }
        .table-panel thead th:nth-child(4), .table-panel tbody td:nth-child(4) { width: 100px; }
        .table-panel thead th:nth-child(5), .table-panel tbody td:nth-child(5) { width: 100px; }
        .table-panel thead th:nth-child(6), .table-panel tbody td:nth-child(6) { width: 150px; }
        .table-panel thead th:nth-child(7), .table-panel tbody td:nth-child(7) { width: 80px; }
        .table-panel thead th:nth-child(8), .table-panel tbody td:nth-child(8) { width: 120px; }
        .table-panel thead th:nth-child(9), .table-panel tbody td:nth-child(9) { width: 100px; }

        .table-panel tbody td input[type="checkbox"] {
            display: block;
            margin: 0 auto;
            width: 16px;
            height: 16px;
        }

        .footer {
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            background-color: #404040;
            padding: 8px;
            border: 1px solid #202020;
            margin-top: 10px;
        }

        .footer-buttons {
            display: flex;
            gap: 10px;
        }

        .footer-button {
            background-color: #E0E0E0;
            border: 1px solid #808080;
            padding: 5px 15px;
            font-size: 14px;
            cursor: pointer;
            text-align: center;
            white-space: nowrap;
            min-width: 80px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            line-height: 1.2;
        }

        .footer-button span {
            font-size: 12px;
        }

        .footer-status {
            background-color: #006633;
            color: white;
            padding: 5px 10px;
            border: 1px solid #004422;
            font-size: 14px;
            white-space: nowrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-left">
                <div class="label-gray">不要出力</div>
                <div class="dark-green-bg title">請求書発行</div>
            </div>
            <div class="header-right">
                <div class="header-item">
                    <div class="label">拠点</div>
                    <div class="dark-green-bg">99</div>
                </div>
                <div class="header-item">
                    <div class="dark-green-bg">全社</div>
                </div>
                <div class="header-item">
                    <div class="label">税率表示</div>
                    <input type="checkbox" id="displayTax">
                    <label for="displayTax">表示</label>
                </div>
                <div class="header-item">
                    <div class="label">請求日付</div>
                    <input type="text" class="input-field date-input" value="2024/02/13(火)">
                    <span class="date-separator">~</span>
                    <input type="text" class="input-field date-input" value="2024/12/19(木)">
                </div>
                <div class="header-item">
                    <div class="label">読込データ件数</div>
                    <div class="dark-green-bg count-display">0</div>
                </div>
            </div>
        </div>

        <div class="main-content">
            <div class="input-panel">
                <div class="input-row">
                    <div class="label">締日※</div>
                    <div class="input-group">
                        <select class="input-field" style="width: 50px;">
                            <option>0</option>
                        </select>
                        <input type="text" class="input-field text-input-full">
                    </div>
                </div>
                <div class="input-row">
                    <div class="label">抽出データ※</div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="2">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="data_extract" value="1">1.売上発生のみ</label>
                            <label class="radio-option"><input type="radio" name="data_extract" value="2" checked>2.売上発生なしを含む</label>
                        </div>
                        <div class="search-input-wrapper">
                            <input type="text" class="input-field" style="border: none; flex-grow: 1;">
                            <div class="search-icon">🔍</div>
                        </div>
                    </div>
                </div>
                <div class="input-row">
                    <div class="label">請求用紙※</div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="1">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="invoice_paper" value="1" checked>1.請求データ作成時/自社</label>
                            <label class="radio-option"><input type="radio" name="invoice_paper" value="2">2.請求データ作成時/指定</label>
                            <label class="radio-option"><input type="radio" name="invoice_paper" value="3">3.自社</label>
                            <label class="radio-option"><input type="radio" name="invoice_paper" value="4">4.指定</label>
                        </div>
                    </div>
                </div>
                <div class="input-row">
                    <div class="label">発行区分※</div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="3">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="issue_category_1" value="1">1.未発行</label>
                            <label class="radio-option"><input type="radio" name="issue_category_1" value="2">2.発行済</label>
                            <label class="radio-option"><input type="radio" name="issue_category_1" value="3" checked>3.全て</label>
                        </div>
                    </div>
                </div>
                <div class="input-row">
                    <div class="label"></div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="3">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="issue_category_2" value="1">1.</label>
                            <label class="radio-option"><input type="radio" name="issue_category_2" value="2">2.</label>
                            <label class="radio-option"><input type="radio" name="issue_category_2" value="3" checked>3.全て</label>
                        </div>
                    </div>
                </div>
                <div class="input-row">
                    <div class="label"></div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="3">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="issue_category_3" value="1">1.</label>
                            <label class="radio-option"><input type="radio" name="issue_category_3" value="2">2.</label>
                            <label class="radio-option"><input type="radio" name="issue_category_3" value="3" checked>3.全て</label>
                        </div>
                    </div>
                </div>
                <div class="input-row">
                    <div class="label">印刷順※</div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="1">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="print_order" value="1" checked>1.フリガナ</label>
                            <label class="radio-option"><input type="radio" name="print_order" value="2">2.取引先CD</label>
                        </div>
                    </div>
                </div>
                <div class="input-row" style="margin-top: 15px;">
                    <div class="label">請求(控)印刷※</div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="3">
                        <div class="radio-group" style="flex-direction: column; align-items: flex-start;">
                            <label class="radio-option"><input type="radio" name="invoice_copy_print" value="1">1.請求書、控えの順で繰返し印刷</label>
                            <label class="radio-option"><input type="radio" name="invoice_copy_print" value="2">2.全ての請求書印刷後、控えを印刷</label>
                            <label class="radio-option"><input type="radio" name="invoice_copy_print" value="3" checked>3.控えを印刷しない</label>
                        </div>
                    </div>
                </div>
                <div class="input-row">
                    <div class="label">請求形態※</div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="1">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="invoice_form" value="1" checked>1.請求データ作成時</label>
                            <label class="radio-option"><input type="radio" name="invoice_form" value="2">2.単月請求</label>
                            <label class="radio-option"><input type="radio" name="invoice_form" value="3">3.繰越請求</label>
                        </div>
                    </div>
                </div>
                <div class="input-row">
                    <div class="label">請求年月日※</div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="1">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="invoice_date_type" value="1" checked>1.締日</label>
                            <label class="radio-option"><input type="radio" name="invoice_date_type" value="2">2.発行日</label>
                            <label class="radio-option"><input type="radio" name="invoice_date_type" value="3">3.無し</label>
                            <label class="radio-option"><input type="radio" name="invoice_date_type" value="4">4.指定</label>
                        </div>
                        <input type="text" class="input-field text-input-full">
                    </div>
                </div>
                <div class="input-row">
                    <div class="label dark-green-bg" style="width: 150px;">請求書発行日※</div>
                    <div class="input-group">
                        <input type="text" class="input-field" value="2" style="width: 30px;">
                        <div class="radio-group">
                            <label class="radio-option"><input type="radio" name="invoice_issue_date" value="1">1.印刷する</label>
                            <label class="radio-option"><input type="radio" name="invoice_issue_date" value="2" checked>2.印刷しない</label>
                        </div>
                    </div>
                </div>
            </div>

            <div class="table-panel">
                <table>
                    <thead>
                        <tr>
                            <th>発行</th>
                            <th>発行済チェック</th>
                            <th>伝票番号</th>
                            <th>請求日付</th>
                            <th>取引先CD</th>
                            <th>取引先名</th>
                            <th>締日</th>
                            <th>前回請求額</th>
                            <th>入金額</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                        <tr><td><input type="checkbox"></td><td><input type="checkbox"></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            <div class="footer-buttons">
                <button class="footer-button">[F1]</button>
                <button class="footer-button">[F5]<span>プレビュー</span></button>
                <button class="footer-button">[F8]<span>検索</span></button>
                <button class="footer-button">[F9]<span>登録</span></button>
                <button class="footer-button">[F12]<span>閉じる</span></button>
            </div>
            <div class="footer-status dark-green-bg">処理No (ESC)</div>
        </div>
    </div>
</body>
</html>
```
    """
    extracted_html = extract_html_content(sample_text)
    print(extracted_html)