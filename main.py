import argparse
import datetime

import pandas as pd

from collections import defaultdict

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


def get_products(path):
    products = (
        pd.read_excel(path)
        .sort_values(['Категория', 'Название'])
        .fillna('')
        .to_dict(orient='records')
    )
    grouped_products = defaultdict(list)

    for product in products:
        category = product.pop('Категория')
        grouped_products[category].append(product)
    return grouped_products


def parse_args():
    parser = argparse.ArgumentParser(description='run wine site')
    parser.add_argument('--path', '-p', help='path to excel file', required=True)
    return parser.parse_args()


def get_template(templates_path='.', template_name='template.html'):
    env = Environment(
        loader=FileSystemLoader(templates_path),
        autoescape=select_autoescape(['html'])
    )
    return env.get_template(template_name)


if __name__ == '__main__':
    args = parse_args()
    template = get_template()

    context = {
        'age': get_age_of_winemaker(),
        'products': get_products(args.path)
    }
    
    rendered_page = template.render(context)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()