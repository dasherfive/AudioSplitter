# AudioSplitter

Windows 本地端音訊自動分割工具 (Auto Audio Splitter)

## 功能
- **自動偵測與分割**：支援 .mp3, .wav, .flac。
- **進度條顯示**：使用 `tqdm` 呈現處理進度。
- **自動環境配置**：自動搜尋 WinGet 安裝的 FFmpeg 路徑。
- **歸檔管理**：自動依原始檔名建立資料夾並有序號化命名。

## 依賴項
- Python 3.10+
- FFmpeg (需安裝於系統或透過 WinGet 安裝)
- Python 套件：
  ```bash
  pip install pydub tqdm
  ```

## 使用方法
```bash
python audio_splitter.py --input_dir "你的音訊資料夾路徑"
```
