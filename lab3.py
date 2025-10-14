from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'аноним'
    age = request.cookies.get('age') or 'неизвестный'
    name_color = request.cookies.get('name_color') or 'blue'
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    pay_error = {}

    price = 0
    drink = request.args.get('drink')
    price = request.args.get('price', type=int, default=0)
    
    if drink:
        if drink == 'coffee':
            price = 120
        elif drink == 'black-tea':
            price = 80
        elif drink == 'green-tea':
            price = 70
        
        if request.args.get('milk') == 'on':
            price += 30
        if request.args.get('sugar') == 'on':
            price += 10
    
    if price == 0:
        return redirect('/lab3/order')

    card = request.args.get('card')
    name = request.args.get('name')
    cvv = request.args.get('CVV')


    if request.args.get('card') is not None or request.args.get('name') is not None or request.args.get('CVV') is not None:

        if not card:
            pay_error['card'] = 'Заполните поле!'
        if not name:
            pay_error['name'] = 'Заполните поле!'
        if not cvv:
            pay_error['cvv'] = 'Заполните поле!'

        if card and name and cvv and not pay_error:
            return redirect(f"/lab3/success?price={price}")

    return render_template('lab3/pay.html',
                           price=price,
                           pay_error=pay_error,
                           card=card,
                           name=name,
                           cvv=cvv)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    fontstyle = request.args.get('fontstyle')

    if color is not None or bgcolor is not None or fontsize is not None or fontstyle is not None:
        resp = make_response(redirect('/lab3/settings'))
        if color is not None:
            resp.set_cookie('color', color)
        if bgcolor is not None:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize is not None:
            resp.set_cookie('fontsize', fontsize)
        if fontstyle is not None:
            resp.set_cookie('fontstyle', fontstyle)
        return resp
    
    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    fontstyle = request.cookies.get('fontstyle')

    resp = make_response(render_template(
        'lab3/settings.html',
        color=color,
        bgcolor=bgcolor,
        fontsize=fontsize,
        fontstyle=fontstyle
    ))
    return resp

@lab3.route('/lab3/reset_style') 
def reset_style(): 
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color') 
    resp.delete_cookie('bgcolor') 
    resp.delete_cookie('fontsize') 
    resp.delete_cookie('fontstyle') 
    return resp

@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    if request.args:
        if not fio:
            errors['fio'] = 'Заполните поле!'
        if not shelf:
            errors['shelf'] = 'Выберите полку!'
        if not linen:
            errors['linen'] = 'Выберите вариант!'
        if not baggage:
            errors['baggage'] = 'Выберите вариант!'
        if not age:
            errors['age'] = 'Заполните поле!'
        elif not age.isdigit() or not (1 <= int(age) <= 120):
            errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
        if not departure:
            errors['departure'] = 'Заполните поле!'
        if not destination:
            errors['destination'] = 'Заполните поле!'
        if not date:
            errors['date'] = 'Выберите дату!'
        if not insurance:
            errors['insurance'] = 'Выберите вариант!'

    if not errors and all([fio, shelf, linen, baggage, age, departure, destination, date, insurance]):
        age_int = int(age)
        if age_int < 18:
            base_price = 700
            ticket_type = 'Детский билет'
        else:
            base_price = 1000
            ticket_type = 'Взрослый билет'
        
        total_price = base_price
        
        if shelf in ['lower', 'lower-side']:
            total_price += 100
        if linen == 'yes':
            total_price += 75
        if baggage == 'yes':
            total_price += 250
        if insurance == 'yes':
            total_price += 150

        return render_template('lab3/ticket_result.html', 
                              fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                              age=age, departure=departure, destination=destination,
                              date=date, insurance=insurance, ticket_type=ticket_type,
                              total_price=total_price)

    return render_template('lab3/ticket.html', 
                          errors=errors, fio=fio, shelf=shelf, linen=linen,
                          baggage=baggage, age=age, departure=departure,
                          destination=destination, date=date, insurance=insurance)

@lab3.route('/lab3/ticket_result')
def ticket_result():
    return redirect('/lab3/ticket')

PRODUCTS = [
    {'id': 1, 'name': 'iPhone 15 Pro', 'brand': 'Apple', 'price': 74000, 'color': 'Титановый', 'storage': '256GB'},
    {'id': 2, 'name': 'Samsung Galaxy S24', 'brand': 'Samsung', 'price': 67000, 'color': 'Черный', 'storage': '128GB'},
    {'id': 3, 'name': 'Xiaomi 14', 'brand': 'Xiaomi', 'price': 60000, 'color': 'Белый', 'storage': '256GB'},
    {'id': 4, 'name': 'Google Pixel 8', 'brand': 'Google', 'price': 30000, 'color': 'Серый', 'storage': '128GB'},
    {'id': 5, 'name': 'OnePlus 12', 'brand': 'OnePlus', 'price': 50000, 'color': 'Зеленый', 'storage': '256GB'},
    {'id': 6, 'name': 'iPhone 14', 'brand': 'Apple', 'price': 42000, 'color': 'Синий', 'storage': '128GB'},
    {'id': 7, 'name': 'Samsung Galaxy A54', 'brand': 'Samsung', 'price': 26000, 'color': 'Фиолетовый', 'storage': '128GB'},
    {'id': 8, 'name': 'Xiaomi Redmi Note 13', 'brand': 'Xiaomi', 'price': 14000, 'color': 'Черный', 'storage': '128GB'},
    {'id': 9, 'name': 'Realme 11 Pro+', 'brand': 'Realme', 'price': 35000, 'color': 'Золотой', 'storage': '256GB'},
    {'id': 10, 'name': 'Nothing Phone 2', 'brand': 'Nothing', 'price': 45000, 'color': 'Белый', 'storage': '128GB'},
    {'id': 11, 'name': 'iPhone SE', 'brand': 'Apple', 'price': 40000, 'color': 'Красный', 'storage': '64GB'},
    {'id': 12, 'name': 'Samsung Galaxy Z Flip5', 'brand': 'Samsung', 'price': 64000, 'color': 'Фиолетовый', 'storage': '256GB'},
    {'id': 13, 'name': 'Xiaomi Poco X6 Pro', 'brand': 'Xiaomi', 'price': 28000, 'color': 'Желтый', 'storage': '256GB'},
    {'id': 14, 'name': 'Google Pixel 7a', 'brand': 'Google', 'price': 41000, 'color': 'Голубой', 'storage': '128GB'},
    {'id': 15, 'name': 'OnePlus Nord 3', 'brand': 'OnePlus', 'price': 35000, 'color': 'Серый', 'storage': '256GB'},
    {'id': 16, 'name': 'iPhone 15 Plus', 'brand': 'Apple', 'price': 61000, 'color': 'Розовый', 'storage': '128GB'},
    {'id': 17, 'name': 'Samsung Galaxy S23 FE', 'brand': 'Samsung', 'price': 40000, 'color': 'Зеленый', 'storage': '128GB'},
    {'id': 18, 'name': 'Xiaomi 13T', 'brand': 'Xiaomi', 'price': 32000, 'color': 'Черный', 'storage': '256GB'},
    {'id': 19, 'name': 'Motorola Edge 40', 'brand': 'Motorola', 'price': 55000, 'color': 'Синий', 'storage': '128GB'},
    {'id': 20, 'name': 'Honor 90', 'brand': 'Honor', 'price': 26000, 'color': 'Серебристый', 'storage': '256GB'}
]

@lab3.route('/lab3/products')
def products():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')

    all_prices = [product['price'] for product in PRODUCTS]
    global_min_price = min(all_prices)
    global_max_price = max(all_prices)
    
    min_price_input = request.args.get('min_price', '')
    max_price_input = request.args.get('max_price', '')
    
    if not min_price_input and min_price_cookie:
        min_price_input = min_price_cookie
    if not max_price_input and max_price_cookie:
        max_price_input = max_price_cookie
    
    try:
        min_price = int(min_price_input) if min_price_input else None
    except ValueError:
        min_price = None
    
    try:
        max_price = int(max_price_input) if max_price_input else None
    except ValueError:
        max_price = None
    
    if min_price is not None and max_price is not None and min_price > max_price:
        min_price, max_price = max_price, min_price
        min_price_input, max_price_input = str(min_price), str(max_price)
    
    
    filtered_products = []
    for product in PRODUCTS:
        price = product['price']
        if min_price is not None and price < min_price:
            continue
        if max_price is not None and price > max_price:
            continue
        filtered_products.append(product)
    
    resp = make_response(render_template(
        'lab3/products.html',
        products=filtered_products,
        min_price=min_price_input,
        max_price=max_price_input,
        filtered_min_price=min_price,
        filtered_max_price=max_price,
        global_min_price=global_min_price,
        global_max_price=global_max_price,
        products_count=len(filtered_products),
        total_count=len(PRODUCTS)
    ))
    
    if request.args:
        if min_price_input:
            resp.set_cookie('min_price', min_price_input)
        else:
            resp.delete_cookie('min_price')
        
        if max_price_input:
            resp.set_cookie('max_price', max_price_input)
        else:
            resp.delete_cookie('max_price')
    
    return resp

@lab3.route('/lab3/products_reset')
def products_reset():
    resp = make_response(redirect('/lab3/products'))
    resp.delete_cookie('min_price')
    resp.delete_cookie('max_price')
    return resp