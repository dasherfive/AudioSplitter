# AudioSplitter

Windows 本地端音訊自動分割工具 (Auto Audio Splitter)

## 目標
開發一支 Python 程式，於 Windows 環境下執行，自動掃描指定目錄，利用靜音偵測技術將串接的長音檔分割為獨立曲目，並依照原始檔名建立目錄進行歸檔。

## 功能
- 自動偵測並分割音訊檔案 (.mp3, .wav, .flac)。
- 支援自定義靜音閾值、最小靜音長度。
- 自動建立目錄並依序號命名分割後的檔案。
- 自動搜尋 Windows 環境下的 FFmpeg 路徑。

## 使用方法
```bash
python audio_splitter.py --input_dir "你的音訊資料夾路徑"
```
