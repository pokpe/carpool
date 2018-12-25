from flask import render_template, request, Blueprint, redirect, url_for
from flask_login import current_user
from carpool.models import Post

main = Blueprint('main', __name__)

@main.before_request
def check_valid_login():
    if not current_user.is_authenticated:
        return redirect(url_for('users.login'))

@main.route("/home")
@main.route("/")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@main.route("/about")
def about():
    return render_template('about.html')
