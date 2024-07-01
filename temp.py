import pysrt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader
import re
from os import listdir


def srt_to_pdf(srt_file, pdf_file):
    subtitles = pysrt.open(srt_file)
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 12)

    y = height - 40
    for subtitle in subtitles:
        text = f"{subtitle.index}\n{subtitle.start} --> {subtitle.end}\n{subtitle.text}\n\n"
        for line in text.split('\n'):
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 12)
                y = height - 40
            c.drawString(40, y, line)
            y -= 20

    c.save()


def pdf_to_srt(pdf_file, srt_file):
    reader = PdfReader(pdf_file)
    content = ""
    for page in reader.pages:
        content += page.extract_text() + "\n"

    subtitle_blocks = re.split(r'\n\s*\n', content.strip())
    with open(srt_file, 'w') as f:
        for block in subtitle_blocks:
            lines = block.strip().split('\n')
            if len(lines) < 3:
                continue
            index = lines[0].strip()
            timecodes = lines[1].strip()
            text = '\n'.join(lines[2:]).strip()
            f.write(f"{index}\n{timecodes}\n{text}\n\n")


# Example usage
srts = listdir("Raw\\srts\\")
for srt in srts:
    srt_to_pdf(srt_file=f"Raw\\srts\\{srt}", pdf_file=f"Raw\\{srt}.pdf")
# pdf_to_srt("output.pdf", "converted.srt")
