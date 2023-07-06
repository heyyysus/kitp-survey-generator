import pdfkit
import db

db_conx = db.connect()
curr = db_conx.cursor()

css_fn = 'style.css'
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


# Render header file
with open(header_fn, 'r') as header:
    data = header.read()
    data = data.format(program_name=program_name)

    with open(rendered_header_fn, 'w') as header_temp:
        header_temp.write(data)
        header_temp.close()
    
    header.close()

# Add rendered header file to options
options = {
    'header-html': rendered_header_fn
}

# Open template file and render to pdf
with open(template_fn, 'r') as f:
    data = f.read()
    data = data.format(folks_table="TABLE")
    pdfkit.from_string(data, 'out.pdf', options=options)