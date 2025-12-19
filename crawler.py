import os
import csv
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
INPUT_FOLDER = r'./original_htmls'
OUTPUT_FILE = 'lyrics_dataset.csv'
# ---------------------

def extract_from_file(file_path):
    """
    Parses a single HTML file to extract Title, Artist, and Lyrics.
    Returns a tuple (title, artist, lyrics) or None if error/empty.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')

        # 1. Extract Title
        title_tag = soup.select_one('.info-wrap .name span')
        title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"

        # 2. Extract Artists
        # Class: text-hide artist-name btn-class hoverLightColor
        artist_tags = soup.find_all(class_="text-hide artist-name btn-class hoverLightColor")
        if artist_tags:
            # Clean and deduplicate artists
            artists = [tag.get_text(strip=True) for tag in artist_tags]
            # Remove duplicates while preserving order
            artists = list(dict.fromkeys(artists)) 
            artist_str = ", ".join(artists)
        else:
            artist_str = "Unknown Artist"

        # 3. Extract Lyrics
        # We search for any div with class "lyrics-box" (ignoring "expanded")
        lyrics_div = soup.select_one(".lyrics-box")
        
        if lyrics_div:
            # Use ". " to separate lines with a dot and a space
            lyrics = lyrics_div.get_text(separator='\n', strip=True)
        else:
            # Return None so we can skip this file in the main loop
            return None

        return title, artist_str, lyrics

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def main():
    count = 0

    with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as outfile:
        # Add minimal labeling columns
        fieldnames = ['id', 'source_file', 'title', 'artist', 'lyrics', 'topic']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()

        if not os.path.exists(INPUT_FOLDER):
            print(f"Error: The folder '{INPUT_FOLDER}' does not exist.")
            return

        for filename in os.listdir(INPUT_FOLDER):
            if filename.lower().endswith(".html"):
                file_path = os.path.join(INPUT_FOLDER, filename)
                result = extract_from_file(file_path)

                if result:
                    title, artist, lyrics = result
                    if not lyrics or lyrics == "[No lyrics found]":
                        continue

                    writer.writerow({
                        'id': os.path.splitext(filename)[0],
                        'source_file': filename,
                        'title': title,
                        'artist': artist,
                        'lyrics': lyrics,
                        'topic': ""  # fill manually later, e.g. "breakup_heartbreak"
                    })

                    count += 1
                    if count % 100 == 0:
                        print(f"Processed {count} songs...")

    print(f"Done! Saved {count} songs to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()