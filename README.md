# _Как запустить проект:_

Клонировать репозиторий и прейти в него в командной строке:

```
git clone https://github.com/filimonka/api_final_yatube.git
```

```
cd api_final_yatube
```

Создать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activte
```
Устаровить зависимости из файла  requirements.txt
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить сервер:
```
python3 manage.py runserver
```
