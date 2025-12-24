import os
import re
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
INPUT_FOLDER = r'./original_htmls'
OUTPUT_FILE = 'lyrics_dataset.txt'
# ---------------------

def extract_lyrics_only(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # Extract Lyrics
        # We search for any div with class "lyrics-box"
        lyrics_div = soup.select_one(".lyrics-box")
        
        if lyrics_div:
            # FASTTEXT REQUIREMENT: Replace newlines with spaces
            lyrics = lyrics_div.get_text(separator=' ', strip=True)
            
            # Clean up extra spaces caused by the replace (and other whitespace)
            lyrics = re.sub(r'\s+', ' ', lyrics)
            return lyrics
        else:
            return None

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def main():
    count = 0

    # utf-8 is required by fastText
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        
        if not os.path.exists(INPUT_FOLDER):
            print(f"Error: The folder '{INPUT_FOLDER}' does not exist.")
            return

        for filename in os.listdir(INPUT_FOLDER):
            if filename.lower().endswith(".html"):
                
                # --- LABEL EXTRACTION ---
                # Remove extension (.html)
                label = os.path.splitext(filename)[0]
                # ------------------------

                file_path = os.path.join(INPUT_FOLDER, filename)
                lyrics = extract_lyrics_only(file_path)

                if lyrics and lyrics != "[No lyrics found]":
                    # Format: __label__<filename> <lyrics>
                    # No title or artist info included.
                    line = f"__label__{label} {lyrics}\n"
                    
                    outfile.write(line)

                    count += 1
                    if count % 100 == 0:
                        print(f"Processed {count} songs...")

    print(f"Done! Saved {count} training examples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()