import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = env.get_template('template.html')

def get_age_of_winemaker():
    foundation_year = 1920
    age_in_years = datetime.date.today().year - foundation_year
    if age_in_years % 10 == 1 and age_in_years % 100 != 11:
        years_word = 'год'
    elif age_in_years % 10 in [2, 3, 4] and age_in_years % 100 not in [12, 13, 14]:
        years_word = 'года'
    else:
        years_word = 'лет'
    return f'{age_in_years} {years_word}'

context = {
    'age': get_age_of_winemaker()
}

rendered_page = template.render(context)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
