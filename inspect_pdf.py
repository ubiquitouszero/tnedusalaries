import sys
import os
import fitz  # PyMuPDF
import pdfplumber

def inspect_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: File {pdf_path} not found.")
        return

    print(f"Inspecting {pdf_path}...")
    
    # 1. Render first page to Image (PNG) using PyMuPDF
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # number of page
        pix = page.get_pixmap()
        output_image = "pdf_preview.png"
        pix.save(output_image)
        print(f"Saved first page image to {output_image}")
        doc.close()
    except Exception as e:
        print(f"Error rendering image: {e}")

    # 2. Extract text with layout using pdfplumber
    try:
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text(layout=True)
            output_text = "pdf_layout.txt"
            with open(output_text, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"Saved text layout to {output_text}")
            
            # Print the first few lines to console for immediate feedback
            print("\n--- Text Preview (First 20 lines) ---")
            lines = text.split('\n')
            for line in lines[:20]:
                print(line)
            print("-------------------------------------")
            
    except Exception as e:
        print(f"Error extracting text: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_pdf.py <pdf_file>")
    else:
        inspect_pdf(sys.argv[1])
