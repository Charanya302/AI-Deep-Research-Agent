from reportlab.pdfgen import canvas

pdf = canvas.Canvas("data/sample.pdf")

pdf.drawString(100, 750, "Artificial Intelligence")
pdf.drawString(100, 720, "AI is a branch of computer science.")
pdf.drawString(100, 690, "Machine Learning is a subset of AI.")
pdf.drawString(100, 660, "Deep Learning uses neural networks.")
pdf.drawString(100, 630, "AI is used in healthcare and education.")

pdf.save()

print("Sample PDF created successfully!")