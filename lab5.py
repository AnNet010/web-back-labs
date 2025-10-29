from flask import Blueprint, render_template, request, make_response, redirect, session
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    username = "anonymous"
    return render_template('lab5/lab5.html', username=username)

@lab5.route('/lab5/login')
def login():
    return "<h2>Страница входа (login)</h2>"

@lab5.route('/lab5/register')
def register():
    return "<h2>Страница регистрации (register)</h2>"

@lab5.route('/lab5/list')
def list_articles():
    return "<h2>Список статей</h2>"

@lab5.route('/lab5/create')
def create_article():
    return "<h2>Создать статью</h2>"