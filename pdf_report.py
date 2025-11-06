from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def make_pdf(symbol, verdict, score, reasons, filename='report.pdf'):
    c= canvas.Canvas(filename, pagesize=letter)
    width, height= letter

    y= height - 60
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50,y, f"Investment Review Report: {symbol}")
    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(50,y, f"Verdict: {verdict} (Score: {score})")
    y -= 30

    c.drawString(50,y, "Reasons:")
    y -= 20

    for r in reasons:
        c.drawString(70,y, f"- {r}")
        y -= 15

    c.showPage()
    c.save()
    return filename