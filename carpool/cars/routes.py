from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from carpool import db
from carpool.models import Car
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
        car = Car(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(car)
        db.session.commit()
        flash('New car has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_car.html', title='New Car', form=form, legend='New Car')
