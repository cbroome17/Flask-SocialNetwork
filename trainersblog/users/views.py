from flask import render_template, url_for, redirect, Blueprint, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from trainersblog import db
from trainersblog.models import User, TrainerPost
from trainersblog.users.image_handler import add_pfp
from trainersblog.users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registers a new user and saves user to the Database
    """
    form = UserRegisterForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """
    Logs in user and redirects them upon successful authentication to home page
    """
    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):

            login_user(user)
            flash('Currently logged in as -PLACEHOLDER-')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('users/login.html', form=form)


@users.route('/logout')
def logout():
    """
    Logouts user
    Redirect to Home
    """
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UserUpdateForm()
    if form.validate_on_submit():

        if form.picture.data:
            # pfp = profile picture
            username = current_user.username
            pfp = add_pfp(form.picture.data, username)
            current_user.profile_image = pfp

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account Successfully Updated!')
        return redirect(url_for('users.account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for(
        'static', filename='profile_pics/' + current_user.profile_image)
    return render_template('users/account.html', profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):
    """
    User public profile. Lists all posts for specified user
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    trainer_posts = TrainerPost.query.filter_by(author=user).order_by(
        TrainerPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('users/user_posts.html', trainer_posts=trainer_posts, user=user)
