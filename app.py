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


flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Анна Боброва'
    return render_template('example.html', name=name)