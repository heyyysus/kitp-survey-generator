import pdfkit
import db
import string
import math

db_conx = db.connect()
curr = db_conx.cursor()

css_fn = 'template/style.css'
template_fn = 'template/body.html'
header_fn = 'template/header.html'
rendered_header_fn = 'template/rendered_header.html'
program_name = 'brainlearn23'


# Fetch people
sql_query = '''select distinct
CONCAT(last_name, ',', ' ', first_name, ' ', '(', short_institution, ')') as 'Display'
from folks_visits
where activity = %s and commit_level in ('a','s','l')
and  person_id != 25627

order by last_name'''

curr.execute(sql_query, [program_name])

people = [person[0] for person in curr]

n = len(people)
mid = math.ceil(n/2)

# Render header file
with open(header_fn, 'r') as header:
    data = header.read()
    data = data.format(program_name=program_name.upper())

    with open(rendered_header_fn, 'w') as header_temp:
        header_temp.write(data)
        header_temp.close()
    
    header.close()

# Add rendered header file to options
options = {
    'header-html': rendered_header_fn
}

# Render table html
table_1_html = '<table id="t1"><tr><th>Prior to the program</th><th>During the program</th><th></th></tr>{}</table>'
table_1_inner = ""

for p in people[ : mid]:
    table_1_inner += "<tr><td></td><td></td><td>{}</td></tr>".format(p)

table_1_html = table_1_html.format(table_1_inner)

table_2_html = '<table id="t2"><tr><th>Prior to the program</th><th>During the program</th><th></th></tr>{}</table>'
table_2_inner = ""

for p in people[mid : ]:
    table_2_inner += "<tr><td></td><td></td><td>{}</td></tr>".format(p)

table_2_html = table_2_html.format(table_2_inner)

table_html = table_1_html + table_2_html

# Open template file and render to pdf
with open(template_fn, 'r') as f:
    data = f.read()
    data = data.format(folks_table=table_html, program_name=program_name.upper())
    pdfkit.from_string(data, 'out.pdf', options=options, css=css_fn)