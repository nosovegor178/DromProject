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

    marks = []
    car_files = []
    # car_images = []
    for root, dirs, files in os.walk('cars'):
        for dir in dirs:
            print(dir)
            if dir != 'media':
                marks.append(dir)
        for file in files:
            if file.endswith('.json'):
                car_files.append(file)
            # else:
            #     car_images.append(file)
    for page_number, car_file in enumerate(car_files):
        path, suffix = os.path.splitext(car_file)
        with codecs.open(f"cars/{path}/{car_file}", "r", "utf_8_sig") as car_info:
            cars_params = car_info.read()
        cars_params = json.loads(cars_params)
        filename, suffix = os.path.splitext(car_file)
        rendered_page = template.render(
            page_number=page_number,
            marks=marks,
            cars=cars_params,
        )

        with open(f"{pages_path}/{filename}.html", 'w', encoding="utf8") as file:
            file.write(rendered_page)


    # print(marks)
    # print(car_files)
    # print(car_images)
    print("Site rebuilt")

on_reload()
server = Server()
server.watch("template.html", on_reload)
server.serve(root='.')
