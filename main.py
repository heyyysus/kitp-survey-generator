import pdfkit

with open('template.html', 'r') as f:
    data = f.read()
    data = data.format(name="BRAINLEARN23")
    pdfkit.from_string(data, 'out.pdf')