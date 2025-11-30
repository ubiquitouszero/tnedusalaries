import sys
import os
import fitz  # PyMuPDF
import pdfplumber

def find_and_inspect_data_page(pdf_path, keyword="Salary"):
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found.")
        return

    print(f"Searching for '{keyword}' in {pdf_path}...")
    
    found_page_num = -1
    
    # Use pdfplumber to find text
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text and keyword.lower() in text.lower():
                found_page_num = i
                print(f"Found '{keyword}' on page {i+1}")
                
                # Extract layout text for this page
                layout_text = page.extract_text(layout=True)
                with open("data_page_layout.txt", "w", encoding="utf-8") as f:
                    f.write(layout_text)
                print(f"Saved text layout of page {i+1} to data_page_layout.txt")
                break
    
    if found_page_num != -1:
        # Render this page to image
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(found_page_num)
            pix = page.get_pixmap()
            output_image = "data_page_preview.png"
            pix.save(output_image)
            print(f"Saved image of page {found_page_num+1} to {output_image}")
            doc.close()
        except Exception as e:
            print(f"Error rendering image: {e}")
    else:
        print(f"Keyword '{keyword}' not found in document.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python find_data_page.py <pdf_file> [keyword]")
    else:
        kw = "Salary"
        if len(sys.argv) > 2:
            kw = sys.argv[2]
        find_and_inspect_data_page(sys.argv[1], kw)
