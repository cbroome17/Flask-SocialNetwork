from flask import flash, redirect, url_for, render_template, Blueprint, abort, request
from flask_login import current_user, login_required
from trainersblog import db
from trainersblog.models import TrainerPost, User
from trainersblog.posts.forms import TrainerPostForm

posts = Blueprint('posts', __name__)


@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """
    User creation of post
    """
    form = TrainerPostForm()

    if form.validate_on_submit():

        post = TrainerPost(
            title=form.title.data,
            text=form.text.data,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template("posts/create.html", form=form)


@posts.route('/<int:post_id>')
@login_required
def post(post_id):
    post = TrainerPost.query.get_or_404(post_id)
    return render_template('posts/post.html',
                           title=post.title, date=post.date, post=post)


@posts.route('/<int:post_id>/update', methods=['GET', 'POST'])
def update(post_id):
    post = TrainerPost.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = TrainerPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('posts.post', post_id=post_id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.text.data = post.text

    return render_template('posts/create.html', title='Updating', form=form)


@posts.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = TrainerPost.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Post Deleted')
    return redirect(url_for('core.index'))


@posts.route('/explore')
@login_required
def view_posts():
    page = request.args.get('page', 1, type=int)
    trainer_posts = TrainerPost.query.filter_by().order_by(
        TrainerPost.date.desc()).paginate(page=page, per_page=10)
    return render_template('posts/explore.html', trainer_posts=trainer_posts)


# trainer_posts = TrainerPost.query.filter_by(author=user).order_by(
#         TrainerPost.date.desc()).paginate(page=page, per_page=5)
