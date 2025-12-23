from flask import Blueprint, render_template, request, session, current_app, abort, jsonify
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)


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


def validate_film(film):
    errors = {}
    if not film.get('title_ru', '').strip():
        errors['title_ru'] = 'Русское название обязательно'
    if not film.get('title_ru', '').strip() and not film.get('title', '').strip():
        errors['title'] = 'Требуется заполнить название'
    try:
        year = int(film.get('year', 0))
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            errors['year'] = f'Год должен быть от 1895 до {current_year}'
    except ValueError:
        errors['year'] = 'Год должен быть числом'
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    return errors


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
        films = cur.fetchall()
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
        films = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id=%s;", (id,))
        film = cur.fetchone()
    else:
        cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id=?;", (id,))
        film = cur.fetchone()
        if film:
            film = dict(film)
    db_close(conn, cur)
    if not film:
        abort(404)
    return jsonify(film)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("DELETE FROM films WHERE id=%s RETURNING id;", (id,))
        deleted = cur.fetchone()
    else:
        cur.execute("DELETE FROM films WHERE id=?;", (id,))
        deleted = cur.rowcount
    db_close(conn, cur)
    if not deleted:
        abort(404)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()

    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400

    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            UPDATE films
            SET title=%s, title_ru=%s, year=%s, description=%s
            WHERE id=%s
            RETURNING id;
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
        updated = cur.fetchone()
    else:
        cur.execute("""
            UPDATE films
            SET title=?, title_ru=?, year=?, description=?
            WHERE id=?
        """, (film['title'], film['title_ru'], film['year'], film['description'], id))
        updated = cur.rowcount
    db_close(conn, cur)

    if not updated:
        abort(404)
    return jsonify(film)
  

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    if not film.get('title', '').strip() and film.get('title_ru', '').strip():
        film['title'] = film['title_ru']

    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400

    conn, cur = db_connect()
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        film_id = cur.fetchone()['id']
    else:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?)
        """, (film['title'], film['title_ru'], film['year'], film['description']))
        film_id = cur.lastrowid
    db_close(conn, cur)

    return jsonify({"id": film_id})