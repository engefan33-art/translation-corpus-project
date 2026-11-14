# 街道之間：提交前操作指南

這是一份可運行的研究網站草稿，尚不是完成所有個人要求的最終提交。

## 預覽

直接雙擊 index.html。資料以 data.js 載入，不需伺服器、套件安裝或網路。來源連結需要連網。

## 已完成

- 500條真實名稱對；固定來源版本及CSV行號；抽樣及清洗腳本。
- 英文／繁體中文介面、報告、編碼手冊與AI聲明。
- 共同篩選的熱力矩陣、分類樹狀矩形圖、雙語語境索引、可排序匯出資料表。
- URL搜尋狀態、矩陣百分比控制、語境列數控制。
- 25條自動試標與50條隨機人工核查表。

## 必須由你完成

1. 開啟 human-review-50.csv，逐條點 source_url，對照固定版本原始資料的名稱及分類。完成後在 verified_by_student 填 yes；記錄 error_found（yes/no）、更正欄及 review_notes。不要把AI檢查當成人工檢查。
2. 將填好的表交回本聊天，以更新語料、統計、人工核查狀態及報告。不要單獨手改 data.json：網站使用 data.js，兩者必須同步。
3. 用自己的話改寫分類定義；讀懂四類的決策順序。補上真實的選題原因、反思、核查日期與錯誤數。少數類別需要額外檢視，25條試標全部屬常見對應。
4. 現有分類描述通名對應，不能在匯報時稱為整條名稱的音譯／意譯比率。

## GitHub Pages 發布

建立你帳戶中的 public repository，例如 hk-street-explorer。把本資料夾內的檔案（而不是外層資料夾）上傳，使 index.html 位於根目錄。Settings → Pages → Deploy from a branch → main → /(root) → Save。等待部署完成，提交網站連結和repository連結。

網站網址通常為 https://你的用戶名.github.io/hk-street-explorer/，這只是格式示例，並非已部署地址。完成核查後再提交。不要上傳私人姓名、學號或核查者個資。

## 重現

Python 3執行 `python build_data.py`；使用本地 source.csv，不需網路。若來源檔不存在則下載固定版本。警告：重跑會重建未核查語料及空白核查表；先備份已填表格。metadata.json記錄SHA-256、排除數、種子及分類總數。

## 授權及來源

原始資料：香港特區政府地政總署；公開資料入口DATA.GOV.HK。下載版本：Martin Chan與貢獻者的hkdatasets（2020快照），固定Git版本見metadata.json。套件DESCRIPTION聲明GPL-3，並表示資料為public domain。保留所有來源與署名。程式及網站以GPL-3.0-or-later提供，資料原有權利不因本專案而改變。來源網址及授權說明見網站參考資料。來源不保證現時完整或正確。
