from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import current_user
from carpool.models import Car, User

main = Blueprint('main', __name__)

@main.before_request
def check_valid_login():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

@main.route("/home")
@main.route("/")
def home():
    cars = Car.query.all()

    for car in cars:
        car.user_one = User.query.filter_by(id=car.member_one).first()
        car.user_two = User.query.filter_by(id=car.member_two).first()
        car.user_three = User.query.filter_by(id=car.member_three).first()
        car.user_four = User.query.filter_by(id=car.member_four).first()
        car.user_five = User.query.filter_by(id=car.member_five).first()

    return render_template('home.html', cars=cars)

@main.route("/about")
def about():
    return render_template('about.html')
