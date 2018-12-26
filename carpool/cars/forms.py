from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class CarForm(FlaskForm):
    title = StringField('Car name', validators=[DataRequired()])
    content = TextAreaField('Members', validators=[DataRequired()])
    submit = SubmitField('Create')
