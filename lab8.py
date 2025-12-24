from flask import Blueprint, render_template, request, session, current_app, abort, jsonify, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__)


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


@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Логин и пароль не могут быть пустыми')

    if users.query.filter_by(login=login_form).first():
        return render_template('lab8/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)
    session['login'] = login_form
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember)
        session['login'] = login_form
        return redirect('/lab8/')

    return render_template('lab8/login.html', error='Ошибка входа')


@lab8.route('/lab8/articles')
def article_list():
    q = request.args.get('q')

    query = articles.query.join(
        users, articles.login_id == users.id
    ).add_columns(
        users.login.label('author_login'),
        articles.id,
        articles.title,
        articles.article_text,
        articles.is_public,
        articles.login_id
    )

    if current_user.is_authenticated:
        query = query.filter(
            (articles.is_public == True) |
            (articles.login_id == current_user.id)
        )
    else:
        query = query.filter(articles.is_public == True)

    if q:
        query = query.filter(
            articles.title.ilike(f'%{q}%') |
            articles.article_text.ilike(f'%{q}%')
        )

    all_articles = query.order_by(articles.id.desc()).all()

    return render_template('lab8/articles.html', articles=all_articles)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if not title or not article_text:
        return render_template('lab8/create.html', error='Заполните все поля')

    new_article = articles(
        title=title,
        article_text=article_text,
        login_id=current_user.id,
        is_public=True,
        is_favorite=False,
        likes=0
    )


    db.session.add(new_article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "Нет доступа", 403

    if request.method == 'GET':
        return render_template(
            'lab8/edit.html',
            article=article
        )

    article.title = request.form.get('title')
    article.article_text = request.form.get('article_text')
    db.session.commit()

    return redirect('/lab8/articles')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "Нет доступа", 403

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles')

@lab8.route('/lab8/toggle_public/<int:article_id>')
@login_required
def toggle_public(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "Нет прав", 403

    article.is_public = not article.is_public
    db.session.commit()
    return redirect('/lab8/articles')
