# AudioSplitter 🎵

Windows 本地端音訊自動分割工具 (Auto Audio Splitter)

這是一個自動化的 Python 工具，能偵測音訊中的靜音區段並自動將其切割為獨立曲目，特別適合處理長篇錄音或數位化的專輯音軌。

## 🚀 快速入門

### 1. 檢視參數說明
若要查看所有可用的參數與預設值，請執行：
```bash
python audio_splitter.py -h
```

### 2. 執行分割任務
針對您的音訊目錄執行基本分割：
```bash
python audio_splitter.py --input_dir "C:\testmusic"
```
*(程式會自動掃描目錄下的 .mp3, .wav, .flac 檔案並開始處理)*

---

## ⚙️ 靈敏度調校指南

如果您發現預設設定無法精準切割（例如：停頓太短、背景雜音干擾），可以透過以下參數調整靈敏度。

### ⚡ 高靈敏度模式 (捕捉極細微停頓)
若要偵測到極短的停頓或微小的音量下降就進行分割，建議指令如下：
```bash
python audio_splitter.py --input_dir "C:\testmusic" --min_silence_len 100 --silence_thresh -30 --keep_silence 50
```

#### 參數細部說明：
*   `--min_silence_len 100`：只要靜音超過 **0.1 秒 (100ms)** 即切割，能捕捉到說話間的細微停頓。
*   `--silence_thresh -30`：提高靜音門檻至 **-30 dBFS** (預設 -40)。表示音量只要低於 -30 dB 就視為靜音，較容易觸發切割。
*   `--keep_silence 50`：切點前後僅保留 **50ms** 緩衝，讓切點更精準（但也可能聽起來較突兀）。

---

## 🛠️ 環境需求

1.  **Python 3.10+**
2.  **FFmpeg**：需安裝於系統或透過 `winget` 安裝。
3.  **Python 套件**：
    ```bash
    pip install pydub tqdm
    ```

## ✨ 主要功能
- **自動環境配置**：自動尋找 WinGet 安裝的 FFmpeg 路徑。
- **雙層進度顯示**：處理大量檔案時提供清晰的進度回饋。
- **智慧歸檔**：依原始檔名建立資料夾，並有序號化命名 (如 `01_filename.mp3`)。

程式已準備就緒，隨時可以開始處理您的音訊收藏！
