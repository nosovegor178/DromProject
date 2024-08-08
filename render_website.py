import codecs
import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')


    pages_path = "car_pages"
    os.makedirs(pages_path, exist_ok=True)

    
    for root, dirs, files in os.walk('cars'):
        for file in files:
            if file.endswith('.json'):
                cars_file = codecs.open(f"{root}/{file}", "r", "utf_8_sig")
                cars_params = cars_file.read()
                cars_file.close()
                cars_params = json.loads(cars_params)
                filename, suffix = os.path.splitext(file)
                rendered_page = template.render(
                    cars=cars_params,
                )

                with open(f"{pages_path}/{filename}.html", 'w', encoding="utf8") as file:
                    file.write(rendered_page)

    print("Site rebuilt")

on_reload()
server = Server()
server.watch("template.html", on_reload)
server.serve(root='.')
