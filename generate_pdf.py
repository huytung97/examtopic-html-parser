import json
import requests
from io import BytesIO
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def fetch_image(url, max_width=400):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        width, height = img.size
        ratio = min(max_width / width, 1)
        img = img.resize((int(width * ratio), int(height * ratio)))
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        return RLImage(img_buffer)
    except Exception as e:
        print(f"Could not load image {url}: {e}")
        return None

def jsonl_to_pdf(jsonl_file, pdf_file):
    styles = getSampleStyleSheet()
    style_bold = ParagraphStyle(
        name='Bold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        spaceAfter=6,
    )
    style_normal = styles['Normal']
    style_choice = ParagraphStyle(
        name='Choice',
        parent=styles['Normal'],
        leftIndent=20,
        spaceAfter=4,
    )
    
    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                            rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    elements = []
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            
            # Add question number
            elements.append(Paragraph(data.get("question_no", "Question"), style_bold))
            
            # Add question text paragraphs
            for paragraph in data.get("text", []):
                elements.append(Paragraph(paragraph, style_normal))
                elements.append(Spacer(1, 6))
            
            # Add images if any
            for img_url in data.get("img", []):
                img = fetch_image(img_url)
                if img:
                    elements.append(img)
                    elements.append(Spacer(1, 12))
            
            # Add choices with indentation
            for choice in data.get("choices", []):
                elements.append(Paragraph(choice, style_choice))
    
    doc.build(elements)
    print(f"PDF generated successfully: {pdf_file}")

# Usage example
jsonl_file = "output.jsonl"  # your input JSONL file
pdf_file = "questions_output.pdf"  # desired output PDF file name

jsonl_to_pdf(jsonl_file, pdf_file)
