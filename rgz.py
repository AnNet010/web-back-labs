from flask import Blueprint, render_template, request, jsonify, session, current_app, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='anna_bobrova_knowledge_base',
            user='anna_bobrova_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()




@rgz.route("/rgz/")
def rgz_index():
    username = session.get('login', "Аноним")
    return render_template('rgz/index.html', username=username)




@rgz.route('/rgz/login')
def login_page():
    return render_template('rgz/login.html')




@rgz.route('/rgz/register')
def register_page():
    return render_template('rgz/register.html')




@rgz.route('/rgz/profile')
def profile_page():
    if 'login_id' not in session:
        return redirect('/rgz/login')
    
    user_id = session['login_id']
    conn, cur = db_connect()
    
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM profiles WHERE user_id=%s;", (user_id,))
    else:
        cur.execute("SELECT * FROM profiles WHERE user_id=?;", (user_id,))
    profile_data = cur.fetchone()
    
    db_close(conn, cur)
    
    if profile_data:
        profile = dict(profile_data) if not isinstance(profile_data, dict) else profile_data
        profile['contact'] = profile.get('contact') or ''
    else:
        profile = None
    
    return render_template('rgz/profile.html', profile=profile)




@rgz.route('/rgz/search')
def search_page():
    if 'login_id' not in session:
        return redirect('/rgz/login')
    return render_template('rgz/search.html')




@rgz.route('/api/register', methods=['POST'])
def api_register():
    
    login = (request.form.get('login') or '').strip()
    password = (request.form.get('password') or '').strip()
    full_name = (request.form.get('full_name') or '').strip()
    age = request.form.get('age')
    gender = request.form.get('gender')
    about = (request.form.get('about') or '').strip()
    contact = (request.form.get('contact') or '').strip()
    has_photo = request.form.get('has_photo') == 'true'

    photo_file = request.files.get('photo')

    if not login or not password or not full_name or not age or not gender:
        return jsonify({"error": "Заполните все обязательные поля"}), 400

    if full_name.isdigit():
        return jsonify({"error": "Полное имя не может быть числом"}), 400

    search_gender = 'Женщина' if gender == 'Мужчина' else 'Мужчина'

    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT login FROM user_new WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM user_new WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn, cur)
        return jsonify({"error": "Такой пользователь уже существует"}), 409

    password_hash = generate_password_hash(password)

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute(
            "INSERT INTO user_new (login, password) VALUES (%s, %s) RETURNING id;",
            (login, password_hash)
        )
        user_id = cur.fetchone()['id']
    else:
        cur.execute(
            "INSERT INTO user_new (login, password) VALUES (?, ?);",
            (login, password_hash)
        )
        user_id = cur.lastrowid


    if photo_file and has_photo:
        from os import path, makedirs
        upload_dir = path.join(path.dirname(path.realpath(__file__)), 'static/uploads')
        makedirs(upload_dir, exist_ok=True)
        filename = f"{user_id}.jpg" 
        photo_file.save(path.join(upload_dir, filename))
        has_photo = True
    else:
        has_photo = False


    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute(
            "INSERT INTO profiles (user_id, full_name, age, gender, search_gender, about, contact, has_photo, is_hidden) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);",
            (user_id, full_name, age, gender, search_gender, about, contact, has_photo, False)
        )
    else:
        cur.execute(
            "INSERT INTO profiles (user_id, full_name, age, gender, search_gender, about, contact, has_photo, is_hidden) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);",
            (user_id, full_name, age, gender, search_gender, about, contact, int(has_photo), 0)
        )

    db_close(conn, cur)
    return jsonify({"message": "Регистрация прошла успешно"}), 201




@rgz.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()

    login_input = data.get('login', '').strip()
    password_input = data.get('password', '').strip()

    if not login_input or not password_input:
        return jsonify({"error": "Заполните все поля"}), 400

    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT * FROM user_new WHERE login=%s;", (login_input,))
    else:
        cur.execute("SELECT * FROM user_new WHERE login=?;", (login_input,))

    user = cur.fetchone()
    db_close(conn, cur)

    if not user:
        return jsonify({"error": "Логин и/или пароль неверны"}), 401

    password_from_db = user['password']
    if isinstance(password_from_db, bytes):
        password_from_db = password_from_db.decode('utf-8')

    if not check_password_hash(password_from_db.strip(), password_input.strip()):
        return jsonify({"error": "Логин и/или пароль неверны"}), 401

    session['login'] = login_input
    session['login_id'] = user['id']
    return jsonify({"message": "Успешный вход", "login": login_input}), 200




@rgz.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('login', None)
    session.pop('login_id', None)
    return jsonify({"message": "Вы успешно вышли из системы"}), 200




@rgz.route('/api/profile', methods=['GET', 'POST', 'DELETE'])
def api_profile():
    if 'login_id' not in session:
        return jsonify({"error": "Пожалуйста, войдите в систему"}), 401

    user_id = session['login_id']
    conn, cur = db_connect()

    if request.method == 'GET':
        
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT * FROM profiles WHERE user_id=%s;", (user_id,))
        else:
            cur.execute("SELECT * FROM profiles WHERE user_id=?;", (user_id,))
        profile_data = cur.fetchone()
        db_close(conn, cur)
        
        if profile_data:
            return jsonify({"profile": dict(profile_data)}), 200
        else:
            return jsonify({"error": "Профиль не найден"}), 404

    elif request.method == 'POST':
 
        full_name = request.form.get('full_name', '').strip()
        age = request.form.get('age')
        gender = request.form.get('gender')
        about = request.form.get('about', '').strip()
        contact = request.form.get('contact', '').strip()
        is_hidden = bool(request.form.get('is_hidden'))

        if not full_name or not age or not gender:
            db_close(conn, cur)
            return jsonify({"error": "Заполните все обязательные поля"}), 400

        try:
            age = int(age)
        except ValueError:
            db_close(conn, cur)
            return jsonify({"error": "Возраст должен быть числом"}), 400

        search_gender = 'Женщина' if gender == 'Мужчина' else 'Мужчина'

        photo_file = request.files.get('photo')
        has_photo = False
        if photo_file:
            upload_dir = path.join(current_app.static_folder, 'uploads')
            if not path.exists(upload_dir):
                from os import makedirs
                makedirs(upload_dir)
            filename = f"{user_id}.jpg"
            upload_path = path.join(upload_dir, filename)
            photo_file.save(upload_path)
            has_photo = True

        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""UPDATE profiles
                           SET full_name=%s, age=%s, gender=%s, search_gender=%s,
                               about=%s, contact=%s, is_hidden=%s, has_photo=%s
                           WHERE user_id=%s;""",
                        (full_name, age, gender, search_gender,
                         about, contact if contact else None, is_hidden, has_photo, user_id))
        else:
            cur.execute("""UPDATE profiles
                           SET full_name=?, age=?, gender=?, search_gender=?,
                               about=?, contact=?, is_hidden=?, has_photo=?
                           WHERE user_id=?;""",
                        (full_name, age, gender, search_gender,
                         about, contact if contact else None, is_hidden, int(has_photo), user_id))

        db_close(conn, cur)
        return jsonify({"message": "Профиль успешно обновлён"}), 200

    elif request.method == 'DELETE':
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("DELETE FROM user_new WHERE id=%s;", (user_id,))
        else:
            cur.execute("DELETE FROM user_new WHERE id=?;", (user_id,))
        db_close(conn, cur)
        session.pop('login', None)
        session.pop('login_id', None)
        return jsonify({"message": "Аккаунт удалён"}), 200




@rgz.route('/api/search', methods=['GET', 'POST'])
def api_search():
    if 'login_id' not in session:
        return jsonify({"error": "Пожалуйста, войдите в систему"}), 401

    user_id = session['login_id']
    
    if request.method == 'GET':
        name = request.args.get('name', '').strip()
        age_str = request.args.get('age', '')
        offset = int(request.args.get('offset', 0))
    else:
        data = request.get_json()
        name = (data.get('name') or '').strip()
        age_str = data.get('age') or ''
        offset = int(data.get('offset') or 0)

    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT gender, search_gender FROM profiles WHERE user_id=%s;", (user_id,))
    else:
        cur.execute("SELECT gender, search_gender FROM profiles WHERE user_id=?;", (user_id,))
    me = cur.fetchone()
    if not me:
        db_close(conn, cur)
        return jsonify({"error": "Профиль не найден"}), 404

    my_gender = me['gender']
    my_search_gender = me['search_gender']

    if current_app.config.get('DB_TYPE') == 'postgres':
        query = """
            SELECT p.user_id, p.full_name, p.age, p.gender, p.about,
                   EXISTS(
                       SELECT 1 FROM likes l
                       WHERE l.from_user_id=%s AND l.to_user_id=p.user_id
                   ) AS liked
            FROM profiles p
            WHERE p.is_hidden = FALSE
              AND p.user_id != %s
              AND p.gender = %s
              AND p.search_gender = %s
        """
        params = [user_id, user_id, my_search_gender, my_gender]
    else: 
        query = """
            SELECT p.user_id, p.full_name, p.age, p.gender, p.about,
                   EXISTS(
                       SELECT 1 FROM likes l
                       WHERE l.from_user_id=? AND l.to_user_id=p.user_id
                   ) AS liked
            FROM profiles p
            WHERE p.is_hidden = 0
              AND p.user_id != ?
              AND p.gender = ?
              AND p.search_gender = ?
        """
        params = [user_id, user_id, my_search_gender, my_gender]

    if name:
        if current_app.config.get('DB_TYPE') == 'postgres':
            query += " AND p.full_name ILIKE %s"
        else:
            query += " AND p.full_name LIKE ?"
        params.append(f"%{name}%")

    if age_str:
        try:
            age = int(age_str)
            if current_app.config.get('DB_TYPE') == 'postgres':
                query += " AND p.age = %s"
            else:
                query += " AND p.age = ?"
            params.append(age)
        except ValueError:
            pass

    if current_app.config.get('DB_TYPE') == 'postgres':
        query += " ORDER BY p.id LIMIT 3 OFFSET %s"
    else:
        query += " ORDER BY p.id LIMIT 3 OFFSET ?"
    params.append(offset)

    cur.execute(query, tuple(params) if current_app.config.get('DB_TYPE') == 'postgres' else params)
    results = cur.fetchall()

    formatted_results = []
    for row in results:
        row_dict = dict(row) if not isinstance(row, dict) else row
        row_dict['liked'] = bool(row_dict.get('liked', False))
        formatted_results.append(row_dict)

    db_close(conn, cur)
    return jsonify({
        "results": formatted_results,
        "offset": offset,
        "filters": {
            "name": name or None,
            "age": age_str or None
        }
    }), 200




@rgz.route('/rgz/logout')
def logout_page():
    session.pop('login', None)
    session.pop('login_id', None)
    return redirect('/rgz/')




@rgz.route('/api/like', methods=['POST'])
def api_like():
    if 'login_id' not in session:
        return jsonify({"error": "Пожалуйста, войдите в систему"}), 401

    data = request.get_json()
    to_user_id = data.get('to_user_id')
    from_user_id = session['login_id']


    if not to_user_id:
        return jsonify({"error": "Не указан пользователь для лайка"}), 400
    try:
        to_user_id = int(to_user_id)
    except ValueError:
        return jsonify({"error": "Некорректный ID пользователя"}), 400

    conn, cur = db_connect()
    try:
 
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                INSERT INTO likes (from_user_id, to_user_id)
                VALUES (%s, %s)
                ON CONFLICT (from_user_id, to_user_id) DO NOTHING;
            """, (from_user_id, to_user_id))
        
            cur.execute("""
                SELECT 1 FROM likes
                WHERE from_user_id=%s AND to_user_id=%s;
            """, (to_user_id, from_user_id))
        else:
            cur.execute("""
                INSERT OR IGNORE INTO likes (from_user_id, to_user_id)
                VALUES (?, ?);
            """, (from_user_id, to_user_id))
            cur.execute("""
                SELECT 1 FROM likes
                WHERE from_user_id=? AND to_user_id=?;
            """, (to_user_id, from_user_id))

        match = cur.fetchone() is not None
        db_close(conn, cur)
        return jsonify({"message": "Лайк отправлен", "match": match}), 200

    except Exception as e:
        db_close(conn, cur)
        return jsonify({"error": str(e)}), 500




@rgz.route('/rgz/my_likes')
def my_likes_page():
    if 'login_id' not in session:
        return redirect('/rgz/login')

    user_id = session['login_id']
    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            SELECT p.user_id, p.full_name, p.age, p.gender
            FROM likes l
            JOIN profiles p ON l.to_user_id = p.user_id
            WHERE l.from_user_id=%s;
        """, (user_id,))
    else:
        cur.execute("""
            SELECT p.user_id, p.full_name, p.age, p.gender
            FROM likes l
            JOIN profiles p ON l.to_user_id = p.user_id
            WHERE l.from_user_id=?;
        """, (user_id,))

    likes = cur.fetchall()
    db_close(conn, cur)
    return render_template('rgz/my_likes.html', likes=likes)




@rgz.route('/api/unlike/<int:user_id>', methods=['POST'])
def unlike_user(user_id):
    if 'login_id' not in session:
        return jsonify({'error': 'Не авторизован'}), 401

    current_user = session['login_id']
    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("DELETE FROM likes WHERE from_user_id=%s AND to_user_id=%s",
                    (current_user, user_id))
    else:
        cur.execute("DELETE FROM likes WHERE from_user_id=? AND to_user_id=?",
                    (current_user, user_id))

    conn.commit()
    db_close(conn, cur)
    return jsonify({'success': True})




@rgz.route('/rgz/matches')
def matches_page():
    if 'login_id' not in session:
        return redirect('/rgz/login')

    user_id = session['login_id']
    conn, cur = db_connect()

    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            SELECT p.user_id, p.full_name, p.age, p.gender, p.contact, p.about
            FROM likes l1
            JOIN likes l2 ON l1.from_user_id = l2.to_user_id AND l1.to_user_id = l2.from_user_id
            JOIN profiles p ON l1.to_user_id = p.user_id
            WHERE l1.from_user_id=%s;
        """, (user_id,))
    else:
        cur.execute("""
            SELECT p.user_id, p.full_name, p.age, p.gender, p.contact, p.about
            FROM likes l1
            JOIN likes l2 ON l1.from_user_id = l2.to_user_id AND l1.to_user_id = l2.from_user_id
            JOIN profiles p ON l1.to_user_id = p.user_id
            WHERE l1.from_user_id=?;
        """, (user_id,))

    matches = cur.fetchall()
    db_close(conn, cur)
    return render_template('rgz/matches.html', matches=matches)

