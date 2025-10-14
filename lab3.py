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
