from albumBand import app
from flask import render_template, flash, redirect, url_for, request
from albumBand.forms import RegistrationForm, LoginForm, PostForm
from albumBand.models import User, Posts
from flask_login import login_required, login_user, logout_user, current_user
import datetime

albums: list[Posts] = [
    Posts('Andrii Babushko', '2018', 'Highway to Hell', '1978'),
    Posts('Ihor Dzhus', '2022', 'Iron Man 2', '2010'),
    Posts('Karina Zbun', '2023', 'Black in Black', '1980'),
    Posts('Olexander Vignich', '2021', 'Power Up', '2020'),
    Posts('Olexander Shumskii', '2015', 'Powerage', '1978')
]

user: User = User()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', albums=albums, user=user)


@app.route('/about/')
def about():
    return render_template('about.html', title='About project', user=user)


@app.route('/about_band/')
def about_band():
    return render_template('about_band.html', title='Band history', user=user)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    login_form: LoginForm = LoginForm()

    if login_form.validate_on_submit():
        if login_form.email.data == 'admin@gmail.com' and login_form.password.data == 'admin':
            init_user('Admin', login_form.email.data, login_form.password.data, True)
            flash('You have been logged in!', 'success')
            return redirect(url_for('index', user=user))
        else:
            flash('Login unsuccessful. Please, check username and password!', 'danger')

    return render_template('login.html', title='Login', form=login_form, user=user)


@app.route("/logout")
def logout():
    logout_user()
    user.is_authenticated = False
    return redirect(url_for('index', user=user))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    registration_form: RegistrationForm = RegistrationForm()

    if registration_form.validate_on_submit():
        init_user(registration_form.username.data, registration_form.email.data, registration_form.password.data, False)
        flash(f'Account was successfully created! Now you are able to log in.', 'success')
        return redirect(url_for('index', user=user))

    return render_template('register.html', title='Registration', form=registration_form, user=user)


@app.route('/post/new', methods=['GET', 'POST'])
def new_post():
    post_form: PostForm = PostForm()

    if post_form.validate_on_submit():
        today = datetime.date.today()
        albums.append(Posts(user.username, today.strftime("%Y"), post_form.title.data, post_form.album_date.data))
        flash('Your post has been created!', 'success')
        return redirect(url_for('index', user=user))

    return render_template('create_post.html', title='New post', form=post_form, user=user, legend='New post')


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id: int):
    searched_album: Posts = get_searched_album(post_id)
    return render_template('post.html', title=searched_album.title, album=searched_album, user=user)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
def update_post(post_id: int):
    searched_album: Posts = get_searched_album(post_id)
    post_form: PostForm = PostForm()

    if post_form.validate_on_submit():
        for album in albums:
            if album.post_id == post_id:
                album.title = post_form.title.data
                album.album_date = post_form.album_date.data
                flash('Your post has been updated!', 'success')
                return redirect(url_for('post', post_id=album.post_id, user=user))
    elif request.method == 'GET':
        post_form.title.data = searched_album.title
        post_form.album_date.data = searched_album.album_date

    return render_template('create_post.html', title='Update post', form=post_form, user=user, legend='Update post')


@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
def delete_post(post_id):
    for album in albums:
        if album.post_id == post_id:
            albums.remove(album)

    flash('Your post has been deleted!', 'success')
    return redirect(url_for('index', user=user))


def init_user(username: str, email: str, password: str, is_authenticated: bool):
    user.username = username
    user.email = email
    user.password = password
    user.is_authenticated = is_authenticated


def get_searched_album(post_id):
    for album in albums:
        if album.post_id == post_id:
            return album
    return None
