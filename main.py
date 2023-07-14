import pdfkit
import db
import string
import math
import os 
import sys
from PyPDF2 import PdfMerger, PdfReader

if not len(sys.argv) == 2:
    print("Use: python3 main.py <PROGRAM_CODE>")
    exit(1)

db_conx = db.connect()
curr = db_conx.cursor()

css_fn = 'template/style.css'
body1_fn = 'template/body1.html'
body2_fn = 'template/body2.html'
header_fn = 'template/header.html'
rendered_header_fn = 'template/rendered_header.html'
program_name = sys.argv[1]


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
mid = math.ceil(n * 0.50)

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
table_1_html = '''<table id="t1">
<colgroup>
       <col span="1" style="width: 18%;">
       <col span="1" style="width: 18%;">
       <col span="1" style="width: 64%;">
</colgroup>
<thead>
    <tr><th>Prior to the program</th><th>During the program</th><th></th></tr>
</thead>
<tbody>
    {}
</tbody>
</table>'''
table_1_inner = ""

for p in people[ : mid]:
    table_1_inner += "<tr><td></td><td></td><td>{}</td></tr>".format(p)

table_1_html = table_1_html.format(table_1_inner)

table_2_html = '''<table id="t2">
<colgroup>
       <col span="1" style="width: 18%;">
       <col span="1" style="width: 18%;">
       <col span="1" style="width: 64%;">
</colgroup>
<thead>
    <tr><th>Prior to the program</th><th>During the program</th><th></th></tr>
</thead>
<tbody>
    {}
</tbody>
</table>'''
table_2_inner = ""

for p in people[mid : ]:
    table_2_inner += "<tr><td></td><td></td><td>{}</td></tr>".format(p)

table_2_html = table_2_html.format(table_2_inner)

table_html = table_1_html + table_2_html

# Make './out' dir if not exists
if not os.path.exists('out'):
    os.makedirs('out')

# Open body files and render to pdfs
with open(body1_fn, 'r') as f:
    data = f.read()
    data = data.format(folks_table=table_html, program_name=program_name.upper())
    pdfkit.from_string(data, 'out/out1.pdf', options=options, css=css_fn)

with open(body2_fn, 'r') as f:
    data = f.read()
    data = data.format(program_name=program_name.upper())
    pdfkit.from_string(data, 'out/out2.pdf', options=options, css=css_fn)

# Merge body pdf files
merger = PdfMerger()

merger.append(PdfReader(open('out/out1.pdf', 'rb')))
merger.append(PdfReader(open('out/out2.pdf', 'rb')))

output = open('out/{}-survey.pdf'.format(program_name), 'wb')
merger.write(output)

merger.close()
output.close()

# Delete temporary out and header files
os.remove('out/out1.pdf')
os.remove('out/out2.pdf')
os.remove('template/rendered_header.html')