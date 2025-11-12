from flask import Blueprint, render_template

lab3 = Blueprint('lab6', __name__)

@lab3.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')
