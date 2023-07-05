from flask import Flask, render_template
from markupsafe import escape
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def index():
    user = "admin"
    friends = ['anne', 'Irish', 'janine']
    return render_template('index.html', user=user, friends=friends)

# localhost:5000/user/<name>
@app.route('/user/<name>')
def hello(name):
    return f"hello, {escape(name)}!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404