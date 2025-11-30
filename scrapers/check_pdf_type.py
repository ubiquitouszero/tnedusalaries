import os

def is_pdf_text_based(filepath):
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
            # Look for common font/text markers in PDF structure
            # This is a very rough heuristic. 
            # If we see /Font and /Text, it's likely text-based.
            # If we see mostly /Image, it might be scanned.
            if b'/Font' in content and b'/Text' not in content: 
                # /Text isn't a standard keyword, but /Type /Font is.
                # Let's just look for a significant amount of text-like bytes? No.
                # Let's look for "stream" blocks which contain text.
                pass
            
            # Better check: look for "Tj" or "TJ" which are text-showing operators in PDF
            if b'Tj' in content or b'TJ' in content:
                return True
            return False
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

pdf_dir = os.path.join("data", "pdfs")
for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        path = os.path.join(pdf_dir, filename)
        is_text = is_pdf_text_based(path)
        print(f"{filename}: {'Text-based (likely)' if is_text else 'Image-based (likely)'}")
