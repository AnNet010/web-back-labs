from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <main>
            <nav>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                </ul>
            </nav>
        </main>
        <footer>
            <p>Боброва Анна Антоновна, ФБИ-31, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1_index():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <p><a href="/">На главную</a></p>

        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/image">/lab1/image</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/counter/reset">/lab1/counter/reset</a></li>
            <li><a href="/lab1/info">/lab1/info</a></li>
            <li><a href="/lab1/created">/lab1/created</a></li>
            <li><a href="/error/400">/error/400</a></li>
            <li><a href="/error/401">/error/401</a></li>
            <li><a href="/error/402">/error/402</a></li>
            <li><a href="/error/403">/error/403</a></li>
            <li><a href="/error/405">/error/405</a></li>
            <li><a href="/error/418">/error/418</a></li>
            <li><a href="/error/500">/error/500</a></li>
        </ul>
    </body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask</h1>
                <a href="/lab1/author">Автор</a>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }
    
@app.route("/lab1/author")    
def author():
    name = "Боброва Анна Антоновна"
    group = "ФБИ-31"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")    
def image():
    path = url_for("static", filename="oak.png")
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
''', 200, {
        "Content-Language": "ru",
        "X-Author": "Anna Bobrova",
        "X-Course": "Web-Programming",
        "X-Group": "FBI-31"
}

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today().strftime("%d.%m.%Y %H:%M:%S")

    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + time + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP адрес: ''' + client_ip + '''<br>
        <a href="/lab1/counter/reset">Сбросить счётчик</a>
    </body>
</html>
'''

@app.route("/lab1/counter/reset")
def reset_counter():
    global count
    count = 0
    return redirect("/lab1/counter")



@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201

log_404 = []

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="error404.css")
    cat1 = url_for("static", filename="errorcat1.png")
    cat2 = url_for("static", filename="errorcat2.png")
    error_img = url_for("static", filename="error404.png")

    ip = request.remote_addr
    url = request.url
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    entry = {"time": now, "ip": ip, "url": url}
    log_404.append(entry)

    log_html = """
    <table style="width:100%; border-collapse:collapse; margin-top:15px; font-family:monospace;">
        <tr style="background:#f0f0f0;">
            <th style="border:1px solid #ccc; padding:5px;">Дата и время</th>
            <th style="border:1px solid #ccc; padding:5px;">Пользователь (IP)</th>
            <th style="border:1px solid #ccc; padding:5px;">Адрес</th>
        </tr>
    """
    for record in reversed(log_404):
        log_html += f"""
        <tr>
            <td style="border:1px solid #ccc; padding:5px;">{record['time']}</td>
            <td style="border:1px solid #ccc; padding:5px;">{record['ip']}</td>
            <td style="border:1px solid #ccc; padding:5px;">{record['url']}</td>
        </tr>
        """
    log_html += "</table>"

    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <link rel="stylesheet" type="text/css" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <img src="{cat1}" class="side-img">
            <img src="{error_img}" class="center-img">
            <img src="{cat2}" class="side-img">
        </div>
        <h1>Упс! Страница потерялась...</h1>
        <p>Но не переживай, котики уже ищут её 🐾</p>
        <a href="/">Вернуться на главную</a>

        <div style="margin-top:80px;">
            <h2>Журнал обращений:</h2>
            {log_html}
        </div>
    </body>
</html>
''', 404


@app.route("/error/400")
def error_400():
    return "400 Bad Request - неправильный, некорректный запрос", 400

@app.route("/error/401")
def error_401():
    return "401 Unauthorized - не авторизован", 401

@app.route("/error/402")
def error_402():
    return "402 Payment Required - необходима оплата", 402

@app.route("/error/403")
def error_403():
    return "403 Forbidden - запрещено (не уполномочен)", 403

@app.route("/error/405")
def error_405():
    return "405 Method Not Allowed - метод не поддерживается", 405

@app.route("/error/418")
def error_418():
    return "418 I'm a teapot - я — чайник", 418

@app.route("/error/500")
def error_500():
    return 10 / 0

@app.errorhandler(500)
def server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Внутренняя ошибка сервера</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #fff3f3;
                text-align: center;
                padding: 50px;
            }
            h1 {
                color: #cc0000;
                font-size: 40px;
            }
            p {
                font-size: 20px;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background: #ffcccc;
                border-radius: 8px;
                text-decoration: none;
                color: black;
                font-weight: bold;
            }
            a:hover {
                background: #ff9999;
            }
        </style>
    </head>
    <body>
        <h1>500 — Внутренняя ошибка сервера</h1>
        <p>На сервере произошла ошибка 😿</p>
        <p>Мы уже работаем над её устранением.</p>
        <a href="/">Вернуться на главную</a>
    </body>
</html>
''', 500

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310},
]

@app.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return render_template(
        'add.html',
        name=name,
        price=price,
        count=len(flower_list),
        flowers=flower_list
    )

@app.route('/lab2/add_flower/')
def add_flower_no_name():
    return render_template('noName.html'), 400


@app.route('/lab2/flowers/')
def show_flowers():
    return render_template('list.html', flowers=flower_list, count=len(flower_list))


@app.route('/lab2/flowers/<int:flower_id>')
def show_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        flower = flower_list[flower_id]
        return render_template('flower.html', flower=flower, flower_id=flower_id)
    else:
        return render_template('flower.html', flower=None, flower_id=flower_id), 404

@app.route('/lab2/clear/')
def clear():
    flower_list.clear()
    return render_template('clear.html', count=len(flower_list))

@app.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        flower_list.pop(flower_id)
        return redirect(url_for('show_flowers'))
    else:
        abort(404)


@app.route('/lab2/add_flower_form')
def add_flower_form():
    name = request.args.get('name')
    price = request.args.get('price', type=int)

    if not name or price is None:
        return render_template('noName.html'), 400

    flower_list.append({'name': name, 'price': price})
    return redirect(url_for('show_flowers'))



@app.route('/lab2/example')
def example():
    name = 'Анна Боброва'
    lab_number = 2
    group = 'ФБИ-31'
    course = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', 
                            name=name, lab_number=lab_number, group=group,
                            course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    division = a / b if b != 0 else None 
    return render_template(
        'calc.html',
        a=a,
        b=b,
        sum=a+b,
        sub=a-b,
        mul=a*b,
        div=division,
        pow=a**b
    )


@app.route('/lab2/calc/')
def calc_one():
    return redirect(url_for('calc', a=1, b=1))

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))

@app.route('/lab2/books/')
def show_books():
    books = [
        {"title": "Война и мир", "author": "Лев Толстой", "genre": "Роман", "pages": 1225},
        {"title": "Преступление и наказание", "author": "Фёдор Достоевский", "genre": "Роман", "pages": 671},
        {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Фантастика", "pages": 470},
        {"title": "Анна Каренина", "author": "Лев Толстой", "genre": "Роман", "pages": 864},
        {"title": "Вишневый сад", "author": "Антон Чехов", "genre": "Драма", "pages": 96},
        {"title": "Горе от ума", "author": "Александр Грибоедов", "genre": "Комедия", "pages": 256},
        {"title": "451 градус по Фаренгейту", "author": "Рэй Брэдбери", "genre": "Фантастика", "pages": 249},
        {"title": "Гарри Поттер и философский камень", "author": "Джоан Роулинг", "genre": "Фэнтези", "pages": 223},
        {"title": "Гамлет", "author": "Уильям Шекспир", "genre": "Драма", "pages": 224},
        {"title": "1984", "author": "Джордж Оруэлл", "genre": "Антиутопия", "pages": 328},
    ]
    return render_template('books.html', books=books)

@app.route('/lab2/cats/')
def cats():
    cats_list = [
        {"name": "Британец", "img": "british.jpg", "desc": "Спокойный и умный кот с плюшевой шерстью."},
        {"name": "Сфинкс", "img": "sphynx.jpg", "desc": "Без шерсти, но очень ласковый и тёплый."},
        {"name": "Мейн-кун", "img": "mainecoon.png", "desc": "Огромный кот, добрый гигант."},
        {"name": "Сиамский", "img": "siamese.jpg", "desc": "Красивый с ярко-голубыми глазами."},
        {"name": "Русская голубая", "img": "russianblue.jpeg", "desc": "Изящная порода с серебристой шерстью."},
        {"name": "Абиссинская", "img": "abyssinian.jpg", "desc": "Активный и игривый охотник."},
        {"name": "Бенгальская", "img": "bengal.jpg", "desc": "Очень энергичная, с пятнистой шерстью как у леопарда."},
        {"name": "Персидская", "img": "persian.jpg", "desc": "Спокойный и пушистый, любит домашний уют."},
        {"name": "Сибирская", "img": "siberian.jpg", "desc": "Крупный и пушистый, прекрасно переносит холод."},
        {"name": "Экзотическая короткошерстная", "img": "exotic.jpg", "desc": "Очень похожа на перса, но с короткой шерстью."},
        {"name": "Ориентальная", "img": "oriental.jpg", "desc": "Худощавое и грациозное создание."},
        {"name": "Шотландская вислоухая", "img": "scottish.jpg", "desc": "Умные и милые с загнутыми ушками."},
        {"name": "Американская короткошерстная", "img": "american.jpg", "desc": "Неприхотливый и здоровый питомец."},
        {"name": "Турецкая ангора", "img": "angora.jpg", "desc": "Изящная белоснежная красавица."},
        {"name": "Бирманская", "img": "birman.jpg", "desc": "Добрый кот с голубыми глазами и белыми лапками."},
        {"name": "Манчкин", "img": "munchkin.jpg", "desc": "Забавные коты с короткими лапками."},
        {"name": "Рэгдолл", "img": "ragdoll.jpg", "desc": "Очень ласковые и спокойные."},
        {"name": "Тайская", "img": "thai.jpg", "desc": "Похожа на сиамскую, но более крепкая."},
        {"name": "Оцикет", "img": "ocicat.jpg", "desc": "Редкая порода, похожа на дикого оцелота."},
        {"name": "Корниш-рекс", "img": "cornish.jpg", "desc": "Имеет мягкую волнистую шерсть."}
    ]
    return render_template('cats.html', cats=cats_list)