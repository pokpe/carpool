from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from carpool import db
from carpool.models import Car, User
from carpool.cars.forms import CarForm

cars = Blueprint('cars', __name__)

@cars.before_request
def check_valid_login():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

@cars.route("/car/new", methods=["GET", "POST"])
@login_required
def new_car():
    form = CarForm()
    if form.validate_on_submit():

        user_one = User.query.filter_by(email=form.member_one.data).first()
        user_two = User.query.filter_by(email=form.member_two.data).first()
        user_three = User.query.filter_by(email=form.member_three.data).first()
        user_four = User.query.filter_by(email=form.member_four.data).first()
        user_five = User.query.filter_by(email=form.member_five.data).first()

        cars.member_one = user_one.id if user_one else ""
        cars.member_two = user_two.id if user_two else ""
        cars.member_three = user_three.id if user_three else ""
        cars.member_four = user_four.id if user_four else ""
        cars.member_five = user_five.id if user_five else ""

        car = Car(car_name=form.car_name.data,
                  member_one=cars.member_one,
                  member_two=cars.member_two,
                  member_three=cars.member_three,
                  member_four=cars.member_four,
                  member_five=cars.member_five)
        db.session.add(car)
        db.session.commit()
        flash('New car has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_car.html', title='New Car', form=form, legend='New Car')

@cars.route("/car/<int:car_id>/update", methods=["GET", "POST"])
@login_required
def update_car(car_id):
    cars = Car.query.get_or_404(car_id)

    if current_user.id != cars.member_one \
    and current_user.id != cars.member_two \
    and current_user.id != cars.member_three \
    and current_user.id != cars.member_four \
    and current_user.id != cars.member_five:
        abort(403)

    form = CarForm()

    if form.validate_on_submit():
        cars.car_name = form.car_name.data

        user_one = User.query.filter_by(email=form.member_one.data).first()
        user_two = User.query.filter_by(email=form.member_two.data).first()
        user_three = User.query.filter_by(email=form.member_three.data).first()
        user_four = User.query.filter_by(email=form.member_four.data).first()
        user_five = User.query.filter_by(email=form.member_five.data).first()

        cars.member_one = user_one.id if user_one else ""
        cars.member_two = user_two.id if user_two else ""
        cars.member_three = user_three.id if user_three else ""
        cars.member_four = user_four.id if user_four else ""
        cars.member_five = user_five.id if user_five else ""

        db.session.commit()
        flash('Your car as been updated', 'success')
        return redirect(url_for('main.home', car_id=cars.id))
    elif request.method == 'GET':

        user_one = User.query.filter_by(id=cars.member_one).first()
        user_two = User.query.filter_by(id=cars.member_two).first()
        user_three = User.query.filter_by(id=cars.member_three).first()
        user_four = User.query.filter_by(id=cars.member_four).first()
        user_five = User.query.filter_by(id=cars.member_five).first()

        form.car_name.data = cars.car_name
        form.member_one.data = user_one.email if user_one else ""
        form.member_two.data = user_two.email if user_two else ""
        form.member_three.data = user_three.email if user_three else ""
        form.member_four.data = user_four.email if user_four else ""
        form.member_five.data = user_five.email if user_five else ""
    return render_template('create_car.html', title='Update Car',
                           form=form, legend='Update Car')


@cars.route("/car/<int:car_id>/delete", methods=["POST"])
@login_required
def delete_car(car_id):
    cars = Car.query.get_or_404(car_id)

    if current_user.id != cars.member_one \
    and current_user.id != cars.member_two \
    and current_user.id != cars.member_three \
    and current_user.id != cars.member_four \
    and current_user.id != cars.member_five:
            abort(403)
    db.session.delete(cars)
    db.session.commit()
    flash('Your car as been deleted', 'success')
    return redirect(url_for('main.home'))
