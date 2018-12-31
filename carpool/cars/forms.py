from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError
from carpool.models import User

class CarForm(FlaskForm):
    car_name = StringField('Car name', validators=[DataRequired(), Length(min=2, max=20)])

    member_one = StringField('Member one',validators=[DataRequired(), Email(), Optional()])
    member_two = StringField('Member two', validators=[Email(), Optional()])
    member_three = StringField('Member three', validators=[Email(), Optional()])
    member_four = StringField('Member four', validators=[Email(), Optional()])
    member_five = StringField('Member five', validators=[Email(), Optional()])

    submit = SubmitField('Save')

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        seen = set()
        for field in [self.member_one, self.member_two, self.member_three, self.member_four, self.member_five]:
            if field.data:
                if field.data in seen:
                    field.errors.append('That email already exists in this car')
                    return False
                else:
                    seen.add(field.data)
                    user = User.query.filter_by(email=field.data).first()
                    if not user:
                        field.errors.append('Account with that email dsnt exist')
                        return False
        return True
