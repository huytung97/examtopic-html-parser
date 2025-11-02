import json
import math
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
import sys
import os


def generate_answer_table_pdf(input_jsonl: str, output_pdf: str, cols: int = 5):
    """
    Generate a PDF answer sheet in table format from a JSONL file.
    Each JSON object must have key: "correct_choices" (list of strings).
    The PDF will display answers in a fixed-width table, with `cols` columns per row.
    """

    if not os.path.exists(input_jsonl):
        print(f"❌ File not found: {input_jsonl}")
        sys.exit(1)

    # Read all answers
    answers = []
    with open(input_jsonl, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            data = json.loads(line)
            correct_choices = data.get("correct_choices", [])
            answer_text = ", ".join(correct_choices)
            answers.append(f"{i}. {answer_text}")

    # Build 2D table (rows × cols)
    rows = math.ceil(len(answers) / cols)
    table_data = []
    for r in range(rows):
        row = []
        for c in range(cols):
            idx = r * cols + c
            row.append(answers[idx] if idx < len(answers) else "")
        table_data.append(row)

    # Setup PDF in portrait orientation
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    # Calculate equal column widths for portrait A4
    page_width = A4[0] - 80  # width minus left/right margins
    col_width = page_width / cols

    table = Table(table_data, colWidths=[col_width] * cols)

    # Style the table
    style = TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ])
    table.setStyle(style)

    # Build PDF
    doc.build([table])
    print(f"✅ PDF generated successfully: {output_pdf}")


if __name__ == "__main__":
    input_path = 'output.jsonl'
    output_path = 'answer.pdf'
    generate_answer_table_pdf(input_path, output_path)
