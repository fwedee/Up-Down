from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    return render_template('index.html')

# Just as a test
@main_blueprint.route('/about')
def about():
    return render_template('about.html')