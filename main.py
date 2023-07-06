import pdfkit
import db

db_conx = db.connect()
curr = db_conx.cursor()

css_fn = 'style.css'
template_fn = 'body.html'
header_fn = 'header.html'
program_name = 'brainlearn23'


# Fetch people
sql_query = '''select distinct # first_name, last_name, 
CONCAT(last_name, ',', ' ', first_name, ' ', '(', short_institution, ')') as 'Display'
from folks_visits
where activity = %s and commit_level in ('a','s','l')
and  person_id != 25627

order by last_name'''.format(program_name)

curr.execute(sql_query, (program_name))


# Render header file
with open(header_fn, 'r') as header:
    data = header.read()
    data = data.format(program_name=program_name)

    with open("{}-temp".format(header_fn), 'w') as header_temp:
        header_temp.write(data)
        header_temp.close()
    
    header.close()

# Add rendered header file to options
options = {
    'header-html': "{}-temp".format(header_fn)
}

# Get people from program

# Open template file and render to pdf
with open(template_fn, 'r') as f:
    data = f.read()
    data = data.format(name="BRAINLEARN23")
    pdfkit.from_string(data, 'out.pdf', options=options)