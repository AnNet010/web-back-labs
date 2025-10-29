from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5

app = Flask(__name__)

app.secret_key = 'секретно-секретный секрет'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

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
                <li><a href="/lab3/">Третья лабораторная</a></li>
                <li><a href="/lab4/">Четвертая лабораторная</a></li>
            </ul>
        </nav>
    </main>
    <footer>
        <p>Боброва Анна Антоновна, ФБИ-31, 3 курс, 2025</p>
    </footer>
</body>
</html>
'''


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