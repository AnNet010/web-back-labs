from flask import Blueprint, render_template, request, make_response, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    login = session.get('login')
    if not login:
        login = "Anonymous"
    return render_template('lab5/lab5.html', username=login)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
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


@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    full_name = request.form.get('full_name', '').strip()

    if not login or not password or not full_name:
        return render_template('lab5/register.html', error='Заполните все поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error="Такой пользователь уже существует")
    
    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (%s, %s, %s);", (login, password_hash, full_name))
    else:
        cur.execute("INSERT INTO users (login, password, full_name) VALUES (?, ?, ?);", (login, password_hash, full_name))
    
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error ='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                                error ='Логин и/или пароль неверны')

    session['login'] = login
    session['login_id'] = user['id']

    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if not title:
        return render_template('lab5/create_article.html', error="Введите название статьи", title=title, article_text=article_text)
    if not article_text:
        return render_template('lab5/create_article.html', error="Введите текст статьи", title=title, article_text=article_text)

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        login_id = cur.fetchone()["id"]
        cur.execute("INSERT INTO articles(user_id, title, article_text) VALUES (%s, %s, %s);",
                    (login_id, title, article_text))

    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        login_id = cur.fetchone()["id"]
        cur.execute("INSERT INTO articles(user_id, title, article_text) VALUES (?, ?, ?);",
                    (login_id, title, article_text))
    
    db_close(conn, cur)
    return redirect('/lab5')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    login_id = session.get('login_id')
    conn, cur = db_connect()

    if login and login_id:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT articles.*, users.login as author_login 
                FROM articles 
                JOIN users ON articles.user_id = users.id 
                WHERE user_id=%s OR is_public=TRUE 
                ORDER BY id DESC;
            """, (login_id,))
        else:
            cur.execute("""
                SELECT articles.*, users.login as author_login 
                FROM articles 
                JOIN users ON articles.user_id = users.id 
                WHERE user_id=? OR is_public=1 
                ORDER BY id DESC;
            """, (login_id,))
    else:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT articles.*, users.login as author_login 
                FROM articles 
                JOIN users ON articles.user_id = users.id 
                WHERE is_public=TRUE 
                ORDER BY id DESC;
            """)
        else:
            cur.execute("""
                SELECT articles.*, users.login as author_login 
                FROM articles 
                JOIN users ON articles.user_id = users.id 
                WHERE is_public=1 
                ORDER BY id DESC;
            """)

    articles = cur.fetchall()
    db_close(conn, cur)
    
    return render_template('lab5/articles.html', 
                         articles=articles, 
                         login_id=login_id)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('login_id', None)
    return redirect('/lab5')


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена", 404

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    if article["user_id"] != login_id:
        db_close(conn, cur)
        return "У вас нет прав на редактирование этой статьи", 403

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        article_text = request.form.get('article_text', '').strip()

        if not title:
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article, error="Введите название статьи")
        if not article_text:
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article, error="Введите текст статьи")

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "UPDATE articles SET title=%s, article_text=%s WHERE id=%s;",
                (title, article_text, article_id)
            )
        else:
            cur.execute(
                "UPDATE articles SET title=?, article_text=? WHERE id=?;",
                (title, article_text, article_id)
            )

        db_close(conn, cur)
        return redirect('/lab5/list')

    db_close(conn, cur)
    return render_template('lab5/edit_article.html', article=article)


@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT user_id FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT user_id FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()
    
    if not article or article["user_id"] != login_id:
        db_close(conn, cur)
        return "У вас нет прав на удаление этой статьи", 403

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/users')
def list_users():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, full_name FROM users ORDER BY id;")
        users = cur.fetchall()
    else:
        cur.execute("SELECT login, full_name FROM users ORDER BY id;")
        users = cur.fetchall()

    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/change_profile', methods=['GET', 'POST'])
def change_profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()


    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return "Пользователь не найден", 404

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '').strip()
        password_confirm = request.form.get('password_confirm', '').strip()

        if password or password_confirm:
            if password != password_confirm:
                db_close(conn, cur)
                return render_template('lab5/change_profile.html', user=user,
                                       error="Пароли не совпадают")
            password_hash = generate_password_hash(password)
        else:
            password_hash = None

        if current_app.config['DB_TYPE'] == 'postgres':
            if password_hash:
                cur.execute(
                    "UPDATE users SET full_name=%s, password=%s WHERE login=%s;",
                    (full_name, password_hash, login)
                )
            else:
                cur.execute(
                    "UPDATE users SET full_name=%s WHERE login=%s;",
                    (full_name, login)
                )
        else:
            if password_hash:
                cur.execute(
                    "UPDATE users SET full_name=?, password=? WHERE login=?;",
                    (full_name, password_hash, login)
                )
            else:
                cur.execute(
                    "UPDATE users SET full_name=? WHERE login=?;",
                    (full_name, login)
                )

        db_close(conn, cur)
        return render_template('lab5/change_success.html', full_name=full_name)

    db_close(conn, cur)
    return render_template('lab5/change_profile.html', user=user)

@lab5.route('/lab5/favorite/<int:article_id>')
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT is_favorite FROM articles WHERE id=%s AND user_id=%s;", (article_id, login_id))
    else:
        cur.execute("SELECT is_favorite FROM articles WHERE id=? AND user_id=?;", (article_id, login_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return "Статья не найдена", 404

    new_status = not article['is_favorite'] if current_app.config['DB_TYPE'] == 'postgres' else not article['is_favorite']
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", (new_status, article_id))
    else:
        cur.execute("UPDATE articles SET is_favorite=? WHERE id=?;", (int(new_status), article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')


@lab5.route('/lab5/toggle_public/<int:article_id>')
def toggle_public(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT is_public, user_id FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT is_public, user_id FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()

    if not article or article['user_id'] != login_id:
        db_close(conn, cur)
        return "У вас нет прав изменять публичность этой статьи", 403

    new_status = not article['is_public']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET is_public=%s WHERE id=%s;", (new_status, article_id))
    else:
        cur.execute("UPDATE articles SET is_public=? WHERE id=?;", (int(new_status), article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')
