from flask import render_template, request, Blueprint

core = Blueprint('core', __name__)


@core.route('/')
def index():
    return render_template('/core/index.html')


@core.route('/about')
def about():
    return render_template('/core/about.html')
