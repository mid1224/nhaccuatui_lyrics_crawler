// ...existing code...
# nhaccuatui_lyrics_crawler

Simple script to extract song metadata and lyrics from saved nhaccuatui.com HTML pages and export them to a CSV dataset.

## Features
- Parse title, artist(s) and lyrics from local .html files
- Export results to a UTF-8 CSV suitable for downstream NLP tasks

## Requirements
- Python 3.8+
- BeautifulSoup4

Install dependencies:
```bash
python3 -m pip install beautifulsoup4
```

## Usage
1. Save nhaccuatui song pages (HTML) into the `original_htmls/` folder.
2. Run the crawler:
   ```bash
   python3 crawler.py
   ```
3. Output file: `lyrics_dataset.csv``