import argparse
import datetime
from collections import defaultdict

import pandas as pd

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape


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

def read_excel(path):
    wines_data = pd.read_excel(path).fillna('').to_dict(orient='records')
    new_format = defaultdict(list)

    for wine_data in wines_data:
        category = wine_data.pop('Категория')
        new_format[category].append(wine_data)
    return new_format


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='run wine site')
    parser.add_argument('--path', '-p', help='path to excel file', required=True)
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    context = {
        'age': get_age_of_winemaker(),
        'wine_cards': read_excel(args.path)
    }
    
    rendered_page = template.render(context)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()