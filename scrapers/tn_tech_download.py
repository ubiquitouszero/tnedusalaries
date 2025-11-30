import os
import requests
import re
from urllib.parse import urljoin

BASE_URL = "https://www.tntech.edu/businessoffice/bpra/budgetary-info.php"
OUTPUT_DIR = os.path.join("data", "pdfs")

def download_pdfs():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"Fetching {BASE_URL}...")
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch page: {e}")
        return

    # Simple regex to find PDF links related to "October" or "July" budgets
    # Looking for href="...pdf" and text containing October or July
    # This is a basic extraction since we don't have BeautifulSoup
    
    # Pattern to find links: <a href="(...pdf)" ...>(...October...|...July...)</a>
    # Note: HTML parsing with regex is fragile, but without bs4 this is a workaround.
    
    content = response.text
    
    # Find all links ending in .pdf
    # This regex looks for href="([^"]+\.pdf)"
    pdf_links = re.findall(r'href="([^"]+\.pdf)"', content, re.IGNORECASE)
    
    print(f"Found {len(pdf_links)} PDF links total.")
    
    downloaded_count = 0
    
    for link in pdf_links:
        # Filter for budget files we care about
        filename = link.split('/')[-1]
        
        # We want "October" or "July" budgets, and recent years (last 10 years approx)
        # Filenames usually look like: October_Budget_Analysis_2024-25.pdf
        if "budget" in filename.lower() and ("october" in filename.lower() or "july" in filename.lower()):
            full_url = urljoin(BASE_URL, link)
            local_path = os.path.join(OUTPUT_DIR, filename)
            
            if os.path.exists(local_path):
                print(f"Skipping {filename} (already exists)")
                continue
                
            print(f"Downloading {filename}...")
            try:
                pdf_resp = requests.get(full_url)
                pdf_resp.raise_for_status()
                with open(local_path, 'wb') as f:
                    f.write(pdf_resp.content)
                downloaded_count += 1
            except Exception as e:
                print(f"Failed to download {full_url}: {e}")

    print(f"Downloaded {downloaded_count} new files.")

if __name__ == "__main__":
    download_pdfs()
