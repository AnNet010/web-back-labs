from flask import Blueprint, render_template, request, session, current_app, abort, jsonify, redirect, make_response
from flask_login import current_user, login_required
import json
import os

lab9 = Blueprint('lab9', __name__)

# Хранилище для открытых коробок
opened_boxes = {}
box_positions = {}

# Список поздравлений (10 уникальных)
congratulations = [
    "С Новым годом! Пусть сбудутся все мечты!",
    "Пусть новый год принесет много радости!",
    "Желаю счастья, здоровья и удачи!",
    "Пусть каждый день нового года будет особенным!",
    "С новыми победами и достижениями!",
    "Пусть год будет полон приятных сюрпризов!",
    "Желаю исполнения самых заветных желаний!",
    "Пусть удача всегда будет на вашей стороне!",
    "С праздником! Пусть год будет ярким!",
    "Желаю мира, добра и благополучия!"
]

# Картинки для коробок (изначально показываются)
initial_presents = [
    "/static/lab9/present1.jpg",
    "/static/lab9/present2.jpg",
    "/static/lab9/present3.jpg",
    "/static/lab9/present4.jpg",
    "/static/lab9/present5.jpg",
    "/static/lab9/present6.jpg",
    "/static/lab9/present7.jpg",
    "/static/lab9/present8.jpg",
    "/static/lab9/present9.jpg",
    "/static/lab9/present10.jpg"
]

# Картинки при открытии (новые фото)
new_presents = [
    "/static/lab9/new1.jpg",
    "/static/lab9/new2.jpg",
    "/static/lab9/new3.jpg",
    "/static/lab9/new4.jpg",
    "/static/lab9/new5.jpg",
    "/static/lab9/new6.jpg",
    "/static/lab9/new7.jpg",
    "/static/lab9/new8.jpg",
    "/static/lab9/new9.jpg",
    "/static/lab9/new10.jpg"
]

# Какие коробки доступны только авторизованным пользователям
REQUIRE_AUTH_FOR = [7, 8, 9]

def get_user_id():
    """Получаем ID пользователя или сессии"""
    if current_user.is_authenticated:
        # Для авторизованных пользователей используем их ID
        user_id = f"user_{current_user.id}"
    else:
        # Для неавторизованных - ID сессии
        if 'anon_id' not in session:
            session['anon_id'] = os.urandom(16).hex()
            # ИНИЦИАЛИЗИРУЕМ счетчик при создании новой анонимной сессии
            session['anon_opened_count'] = 0
        user_id = f"anon_{session['anon_id']}"
    
    return user_id

def get_opened_count(user_id):
    """Получаем количество открытых коробок для пользователя"""
    if current_user.is_authenticated:
        # Для авторизованных храним в словаре
        if user_id not in opened_boxes:
            opened_boxes[user_id] = {'boxes': [], 'count': 0}
        return opened_boxes[user_id]['count']
    else:
        # Для неавторизованных храним в сессии
        return session.get('anon_opened_count', 0)

def set_opened_count(user_id, count):
    """Устанавливаем количество открытых коробок для пользователя"""
    if current_user.is_authenticated:
        if user_id not in opened_boxes:
            opened_boxes[user_id] = {'boxes': [], 'count': 0}
        opened_boxes[user_id]['count'] = count
    else:
        session['anon_opened_count'] = count

def get_opened_boxes(user_id):
    """Получаем список открытых коробок"""
    if current_user.is_authenticated:
        if user_id not in opened_boxes:
            opened_boxes[user_id] = {'boxes': [], 'count': 0}
        return opened_boxes[user_id]['boxes']
    else:
        # Для неавторизованных храним в сессии
        if 'anon_opened_boxes' not in session:
            session['anon_opened_boxes'] = []
        return session['anon_opened_boxes']

def add_opened_box(user_id, box_id):
    """Добавляем открытую коробку"""
    if current_user.is_authenticated:
        if user_id not in opened_boxes:
            opened_boxes[user_id] = {'boxes': [], 'count': 0}
        opened_boxes[user_id]['boxes'].append(box_id)
    else:
        if 'anon_opened_boxes' not in session:
            session['anon_opened_boxes'] = []
        session['anon_opened_boxes'].append(box_id)

def init_user_boxes(user_id):
    """Инициализируем данные для пользователя"""
    # Инициализируем список открытых коробок
    get_opened_boxes(user_id)
    
    if user_id not in box_positions:
        # ФИКСИРОВАННЫЕ позиции как в задании
        positions = [
            {'id': 0, 'top': 10, 'left': 5, 'zIndex': 1, 'initial_image': initial_presents[0], 'requires_auth': False},
            {'id': 1, 'top': 10, 'left': 30, 'zIndex': 1, 'initial_image': initial_presents[1], 'requires_auth': False},
            {'id': 2, 'top': 35, 'left': 17, 'zIndex': 1, 'initial_image': initial_presents[2], 'requires_auth': False},
            {'id': 3, 'top': 25, 'left': 80, 'zIndex': 1, 'initial_image': initial_presents[3], 'requires_auth': False},
            {'id': 4, 'top': 15, 'left': 55, 'zIndex': 1, 'initial_image': initial_presents[4], 'requires_auth': False},
            {'id': 5, 'top': 50, 'left': 37, 'zIndex': 1, 'initial_image': initial_presents[5], 'requires_auth': False},
            {'id': 6, 'top': 60, 'left': 5, 'zIndex': 1, 'initial_image': initial_presents[6], 'requires_auth': False},
            {'id': 7, 'top': 65, 'left': 60, 'zIndex': 1, 'initial_image': initial_presents[7], 'requires_auth': True},
            {'id': 8, 'top': 80, 'left': 21, 'zIndex': 1, 'initial_image': initial_presents[8], 'requires_auth': True},
            {'id': 9, 'top': 70, 'left': 85, 'zIndex': 1, 'initial_image': initial_presents[9], 'requires_auth': True},
        ]
        box_positions[user_id] = positions

def get_remaining_boxes_count(user_id):
    """Получаем количество неоткрытых коробок"""
    init_user_boxes(user_id)
    opened_boxes_list = get_opened_boxes(user_id)
    return 10 - len(opened_boxes_list)

@lab9.route('/lab9/', methods=['GET'])
def main():
    user_id = get_user_id()
    init_user_boxes(user_id)
    
    positions = box_positions[user_id]
    opened_count = get_opened_count(user_id)
    remaining_count = get_remaining_boxes_count(user_id)
    
    return render_template(
        'lab9/index.html',
        positions=positions,
        remaining=remaining_count,
        opened_count=opened_count,
        is_authenticated=current_user.is_authenticated,
        username=current_user.login if current_user.is_authenticated else None
    )

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    user_id = get_user_id()
    data = request.get_json()

    if not data or 'box_id' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    box_id = int(data['box_id'])
    init_user_boxes(user_id)
    
    # Проверка на авторизацию для специальных коробок
    if box_id in REQUIRE_AUTH_FOR and not current_user.is_authenticated:
        return jsonify({'error': 'Эта коробка доступна только авторизованным пользователям'}), 403
    
    # Проверка, открыта ли уже коробка
    opened_boxes_list = get_opened_boxes(user_id)
    if box_id in opened_boxes_list:
        return jsonify({'error': 'Эта коробка уже открыта'}), 400
    
    # Проверка лимита (3 коробки)
    if get_opened_count(user_id) >= 3:
        return jsonify({'error': 'Вы уже открыли максимальное количество коробок (3)'}), 400
    
    # Открываем коробку
    add_opened_box(user_id, box_id)
    
    # Увеличиваем счетчик
    new_count = get_opened_count(user_id) + 1
    set_opened_count(user_id, new_count)
    
    return jsonify({
        'success': True,
        'congratulation': congratulations[box_id],
        'gift': new_presents[box_id],
        'opened': new_count,
        'remaining': get_remaining_boxes_count(user_id)
    })

@lab9.route('/lab9/santa', methods=['POST'])
@login_required
def santa_refill():
    """Дед Мороз наполняет все коробки (только для авторизованных)"""
    user_id = f"user_{current_user.id}"
    
    # Очищаем открытые коробки и счетчик
    if user_id in opened_boxes:
        opened_boxes[user_id] = {'boxes': [], 'count': 0}
    
    return jsonify({
        'success': True,
        'message': 'Дед Мороз наполнил все коробки новыми подарками!'
    })

@lab9.route('/lab9/reset', methods=['POST'])
def reset():
    """Сброс для неавторизованных пользователей"""
    if current_user.is_authenticated:
        return jsonify({'error': 'Авторизованные пользователи используют кнопку "Дед Мороз"'}), 403
    
    # Сбрасываем данные для неавторизованного пользователя
    session['anon_opened_count'] = 0
    session['anon_opened_boxes'] = []
    
    # Также очищаем из хранилища по старому ID
    old_user_id = f"anon_{session.get('anon_id', '')}"
    if old_user_id in opened_boxes:
        del opened_boxes[old_user_id]
    if old_user_id in box_positions:
        del box_positions[old_user_id]
    
    # Генерируем новый ID для сессии
    session['anon_id'] = os.urandom(16).hex()
    
    return jsonify({
        'success': True,
        'message': 'Игра сброшена! Теперь можно открыть 3 новые коробки.'
    })