from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.forms import RegristrationForm, LoginForm, RssFeed, deleteFeeds
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.filter_by(user_id=current_user.get_id())
    return render_template('home.html',title='Home', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/addfeed', methods=['GET', 'POST'])
@login_required
def addfeed():
    addForm = RssFeed()
    deleteForm = deleteFeeds()
    if addForm.submit1.data and addForm.validate_on_submit():
        post = Post(title=addForm.title.data, link=addForm.link.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('New feed added','success')
        return redirect(url_for('home'))
    if deleteForm.validate_on_submit():
        db.session.query(Post).filter_by(user_id=current_user.get_id()).delete()
        db.session.commit()
        flash('All feeds cleared','success')
        return redirect(url_for('home'))
    return render_template('addfeed.html', title='Add Feed', addForm=addForm, deleteForm=deleteForm)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegristrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. please check your details and try again.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))