from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime


lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
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

@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return render_template(
        'lab2/add.html',
        name=name,
        price=price,
        count=len(flower_list),
        flowers=flower_list
    )

@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return render_template('lab2/noName.html'), 400


@lab2.route('/lab2/flowers/')
def show_flowers():
    return render_template('lab2/list.html', flowers=flower_list, count=len(flower_list))


@lab2.route('/lab2/flowers/<int:flower_id>')
def show_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        flower = flower_list[flower_id]
        return render_template('lab2/flower.html', flower=flower, flower_id=flower_id)
    else:
        return render_template('lab2/flower.html', flower=None, flower_id=flower_id), 404

@lab2.route('/lab2/clear/')
def clear():
    flower_list.clear()
    return render_template('lab2/clear.html', count=len(flower_list))

@lab2.route('/lab2/flowers/delete/<int:flower_id>')
def delete_flower(flower_id):
    if 0 <= flower_id < len(flower_list):
        flower_list.pop(flower_id)
        return redirect(url_for('lab2.show_flowers'))
    else:
        abort(404)

@lab2.route('/lab2/add_flower_form')
def add_flower_form():
    name = request.args.get('name')
    price = request.args.get('price', type=int)

    if not name or price is None:
        return render_template('lab2/noName.html'), 400

    flower_list.append({'name': name, 'price': price})
    return redirect(url_for('lab2.show_flowers'))

@lab2.route('/lab2/example')
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
    return render_template('lab2/example.html', 
                            name=name, lab_number=lab_number, group=group,
                            course=course, fruits=fruits)

@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase = phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    division = a / b if b != 0 else None 
    return render_template(
        'lab2/calc.html',
        a=a,
        b=b,
        sum=a+b,
        sub=a-b,
        mul=a*b,
        div=division,
        pow=a**b
    )

@lab2.route('/lab2/calc/')
def calc_one():
    return redirect(url_for('lab2.calc', a=1, b=1))

@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('lab2.calc', a=a, b=1))

@lab2.route('/lab2/books/')
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
    return render_template('lab2/books.html', books=books)

@lab2.route('/lab2/cats/')
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
    return render_template('lab2/cats.html', cats=cats_list)