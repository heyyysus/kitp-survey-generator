import pdfkit
import db

db_conx = db.connect()

css_fn = 'style.css'
template_fn = 'template.html'


with open(template_fn, 'r') as f:
    data = f.read()
    data = data.format(name="BRAINLEARN23")
    pdfkit.from_string(data, 'out.pdf')