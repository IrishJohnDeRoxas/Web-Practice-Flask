# import os
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# from markupsafe import escape

app = Flask(__name__)
# Add database 

# Sqlite db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(app.root_path, 'users.db')

# Mysql db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Biboy_321@localhost/flask_db'

# Secret key
app.config['SECRET_KEY'] = 'IJD'
#  Initialize Db
db = SQLAlchemy(app)
app.app_context().push()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Create String
    def __repr__(self):
        return '<Name %r>' % self.name


class EditTextForm(FlaskForm):
    name = StringField('Text: ', validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserForm(FlaskForm):
    name = StringField('Name ', validators=[DataRequired()])
    email = StringField('Email ', validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/users', methods=['GET', 'POST'])
def users():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            form.name.data = ''
            form.email.data = ''
            flash("Added")
        else:
            flash("Email is already in use")

        name = form.name.data
    our_users = Users.query.order_by(Users.date_added)
    return render_template('users.html', name=name, form=form, our_users=our_users)


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    name_to_update = Users.query.get_or_404(id)
    form = UserForm(obj=name_to_update)
    if form.validate_on_submit():
        form.populate_obj(name_to_update)
        try:
            db.session.commit()
            flash('Update success')
            return redirect(url_for('users'))
        except:
            flash('Error')
            return render_template('update.html', form=form, name_to_update=name_to_update)
    return render_template('update.html', form=form, name_to_update=name_to_update)


#
# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     form = UserForm()
#     name_to_update = Users.query.get_or_404(id)
#     if request.method == 'POST':
#         name_to_update.name = request.form['name']
#         name_to_update.email = request.form['email']
#         try:
#             db.session.commit()
#             flash('Update success')
#             return render_template('update.html', form=form, name_to_update=name_to_update)
#         except:
#             flash('Error')
#             return render_template('update.html', form=form, name_to_update=name_to_update)
#     else:
#         return render_template('update.html', form=form, name_to_update=name_to_update)


@app.route('/edit-text', methods=['GET', 'POST'])
def edit_text():
    name = None
    form = EditTextForm()
    # validate form
    if form.validate_on_submit():
        name = form.name.data.replace(" ", "🤸") + "🤸🤸🤸"
        form.name.data = ''
        flash("Success")
    return render_template('simple_projects/edit_text.html', name=name, form=form)


@app.route('/css-flexbox')
def flexbox():
    return render_template('css_practice/css_flexbox.html')


@app.route('/css-table')
def table():
    return render_template('css_practice/table.html')


@app.route('/resume')
def resume():
    return render_template('simple_projects/resume.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(debug=True)
