import fitz
import os
import sys

def convert_pdf_to_html_gallery(pdf_path, output_dir="pdf_gallery"):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = fitz.open(pdf_path)
    filename = os.path.basename(pdf_path)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{filename}</title>
        <style>
            body {{ font-family: sans-serif; background: #f0f0f0; text-align: center; padding: 20px; }}
            .page {{ margin: 20px auto; box-shadow: 0 0 10px rgba(0,0,0,0.1); max-width: 100%; }}
            img {{ max-width: 100%; height: auto; }}
        </style>
    </head>
    <body>
        <h1>{filename}</h1>
    """

    print(f"Converting {len(doc)} pages...")
    # Limit to first 20 pages to avoid huge generation time for now, or do all if small.
    # Let's do first 20 for speed.
    max_pages = 20
    for i in range(min(len(doc), max_pages)):
        page = doc.load_page(i)
        pix = page.get_pixmap()
        img_filename = f"page_{i+1}.png"
        img_path = os.path.join(output_dir, img_filename)
        pix.save(img_path)
        
        html_content += f"""
        <div class="page">
            <h3>Page {i+1}</h3>
            <img src="{img_filename}" alt="Page {i+1}">
        </div>
        """
        print(f"Saved {img_filename}")

    if len(doc) > max_pages:
        html_content += f"<p>... and {len(doc) - max_pages} more pages.</p>"

    html_content += "</body></html>"

    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w") as f:
        f.write(html_content)
    
    print(f"Gallery created at {html_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_html.py <pdf_path>")
    else:
        convert_pdf_to_html_gallery(sys.argv[1])
