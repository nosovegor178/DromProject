# Сайт с автомобилями с spb.drom.ru

Этот проект создаёт сайт с выборкой автомобилей определённых марок из города Санкт-Петербург. Все автомобили берутся с сайта [spb.drom.ru](https://spb.drom.ru).

### Как установить

Рекомендуется использовать [virtulenv/venv](https://docs.pythpn.org/3/library/venv.html) для изоляции проекта.

На компьютере пользователя должен быть установлен Python3.
Затем используйте `pip` (или `pip3`, есть конфликт Python2) для установки зависимостей:
```
pip install -r requirments.txt
``` 

### Пример запуска
Для запуска Вам потребуется перейти в командной строке в месторасположение программы и сначала запустить парсер:
```
python parsing.py
```
После этого нужно запустить сам сервер командой:
```
python render_website.py
```
После этого перейдите по ссылке [http://127.0.0.1:5500/car_pages/index/index.html](http://127.0.0.1:5500/car_pages/index/index.html), чтобы открыть сайт.

### Цель проекта

Код написан в образовательных целях на совместном проекте для веб-разработчиков от школы [Третье место](https://3place.ru).