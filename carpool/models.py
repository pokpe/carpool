from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from carpool import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "User('{}, {}, {}')".format(self.username, self.email, self.image_file)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Post('{}, {}')".format(self.title, self.date_posted)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    car_name = db.Column(db.String(100), nullable=False)

    member_one = db.Column(db.Integer, nullable=False)
    member_two = db.Column(db.Integer, nullable=True)
    member_three = db.Column(db.Integer, nullable=True)
    member_four = db.Column(db.Integer, nullable=True)
    member_five = db.Column(db.Integer, nullable=True)

    week_day_one = db.Column(db.Integer, nullable=True)
    week_day_two = db.Column(db.Integer, nullable=True)
    week_day_three = db.Column(db.Integer, nullable=True)
    week_day_four = db.Column(db.Integer, nullable=True)
    week_day_five = db.Column(db.Integer, nullable=True)

    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return "Car('{}, {}, {}, {}, {}, {}')".format(self.car_name,
                                                      self.member_one,
                                                      self.member_two,
                                                      self.member_three,
                                                      self.member_four,
                                                      self.member_five)
