import codecs
import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import random


def on_reload():
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")

    pages_path = "car_pages"
    os.makedirs(pages_path, exist_ok=True)

    marks = []
    car_files = []
    for root, dirs, files in os.walk("cars"):
        for dir in dirs:
            if dir != "media":
                marks.append(dir)
        for file in files:
            if file.endswith(".json"):
                car_files.append(file)
    for car_file in (car_files):
        path, suffix = os.path.splitext(car_file)
        new_path = f"{pages_path}/{path}"
        os.makedirs(new_path, exist_ok=True)
        with codecs.open(f"cars/{path}/{car_file}", "r", "utf_8_sig") as car_info:
            cars_params = car_info.read()
        filename, suffix = os.path.splitext(car_file)
        all_cars_params = json.loads(cars_params)
        cars_params = list(chunked(all_cars_params, 20))
        pages_count = len(cars_params)
        for page_number, car_params in enumerate(cars_params, 1): 
            rendered_page = template.render(
                page_number=page_number,
                pages_count=pages_count,
                marks=marks,
                filename=filename,
                cars=car_params,
            )
            with open(f"{new_path}/{filename}{page_number}.html", "w", encoding="utf8") as file:
                file.write(rendered_page)
        
    index_path = f'{pages_path}/index'
    os.makedirs(index_path, exist_ok=True)
    random_dirs = random.sample(os.listdir('cars'), 4)
    random_cars = []
    for random_dir in random_dirs:
        path = f"cars/{random_dir}/{random_dir}.json"
        with codecs.open(path, "r", "utf_8_sig") as car_info:
            cars_params = car_info.read()
        cars_params = json.loads(cars_params)
        random_cars.extend(random.sample(cars_params, 5))
        random.shuffle(random_cars)
    rendered_page = template.render(
        page_number=1,
        pages_count=1,
        marks=marks,
        cars=random_cars,
    )
    with open("car_pages/index/index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)
    

on_reload()
server = Server()
server.watch("template.html", on_reload)
server.serve(root=".")