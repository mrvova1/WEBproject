from flask import Flask, render_template, redirect, make_response, jsonify, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_restful import reqparse, abort, Api, Resource
from data import db_session, users_resource, news_api
from data.add_team import AddTeamForm
from data.add_glava import AddGlavaForm
from data.login_form import LoginForm
from data.add_manga import AddMangaForm
from data.manga import Manga
from data.users import User
from data.teams import Teams
from data.register import RegisterForm
import os.path
from zipfile import ZipFile

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
MAX_CONTENT_LENGTH = 1024 * 1024 * 1024
img = None

login_manager = LoginManager()
login_manager.init_app(app)

# для списка объектов
api.add_resource(users_resource.NewsListResource, '/api/v2/users')

# для одного объекта
api.add_resource(users_resource.NewsResource, '/api/v2/users/<int:user_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global img
    if request.method == 'POST':
        file = request.files['file']
        try:
            img = file.read()
        except FileNotFoundError as e:
            pass
    else:
        pass
    return None


@app.route('/addglava', methods=['GET', 'POST'])
def addglava():
    addglav = AddGlavaForm()
    if request.method == 'POST':
        file = request.files['file']
        try:
            with ZipFile(file) as myzip:
                a = 0
                db_sess = db_session.create_session()
                manga = db_sess.query(Manga).all()
                n = manga[addglav.id.data - 1].Number_of_chapters
                num_rows_updated = db_sess.query(Manga).filter_by(id=(addglav.id.data)).update(
                    dict(Number_of_chapters=(n + 1)))
                db_sess.commit()
                os.mkdir(f'Manga/{addglav.id.data}/{n + 1}')
                for i in myzip.namelist():
                    with myzip.open(i, 'r') as img:
                        img = img.read()
                        o = open(f'Manga/{addglav.id.data}/{n + 1}/{a}.png', 'wb')
                        a += 1
                        o.write(img)
                        o.close()
        except FileNotFoundError as e:
            pass
    else:
        pass
    return render_template('addglava.html', title='Добавление главы', form=addglav)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
@app.route("/manga")
def manga():
    db_sess = db_session.create_session()
    manga = db_sess.query(Manga).all()
    manga.reverse()
    return render_template("manga.html", manga=manga, title='Manga')


@app.route("/teamlist")
def teamlist():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Teams).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names, title='Interpritator teams')


@app.route('/poluchenie_oblojki/<int:num>', methods=['GET', 'POST'])
def poluchenie_oblojki(num):
    db_sess = db_session.create_session()
    manga = db_sess.query(Manga).all()
    i = manga[num - 1]
    img = i.Oblojka
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route("/manga/<int:teg>/<int:glava>")
def mangar(teg, glava):
    db_sess = db_session.create_session()
    manga = db_sess.query(Manga).all()
    name = manga[teg - 1].name
    kolvo_glav = manga[teg - 1].Number_of_chapters
    id = manga[teg - 1].id
    try:
        path = f'Manga/{id}/{glava}'
        ctr = len([f for f in os.listdir(path)
                   if os.path.isfile(os.path.join(path, f))])
        return render_template("manga_read.html", kolvo_glav=kolvo_glav, ctr=ctr, glava=glava, name=name, id=id,
                               title='Interpritator teams')
    except BaseException:
        return redirect('/')


@app.route("/zagruzka_glavi/<int:id>/<int:glava>/<int:ctr>")
def zagruzka_glavi(id, glava, ctr):
    img = open(f'Manga/{id}/{glava}/{ctr}.png', 'rb').read()
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            age=form.age.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addteam', methods=['GET', 'POST'])
def addteam():
    mes = ''
    add_form = AddTeamForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        team = Teams(
            name=add_form.name.data,
            Line_up=add_form.Line_up.data,
            Permissions=add_form.Permissions.data
        )
        try:
            db_sess.add(team)
            db_sess.commit()
            return redirect('/')
        except BaseException:
            mes = 'Name is already exist'
    return render_template('addteam.html', title='Adding a team', form=add_form, message=mes)


@app.route('/addmanga', methods=['GET', 'POST'])
def addmanga():
    global img
    add_form = AddMangaForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        upload()
        manga = Manga(
            name=add_form.name.data,
            Release_year=add_form.Release_year.data,
            Title_status=add_form.Title_status.data,
            Translation_status='Продолжается',
            Author=add_form.Author.data,
            Artist=add_form.Artist.data,
            Interpritator_team=add_form.Interpritator_team.data,
            Number_of_chapters=add_form.Number_of_chapters.data,
            Oblojka=img
        )
        db_sess.add(manga)
        db_sess.commit()
        manga = db_sess.query(Manga).all()
        for i in manga:
            if i.Oblojka == img:
                id_for_file = i.id
        os.mkdir(f'Manga/{id_for_file}')
        img = None
        return redirect('/')
    return render_template('addmanga.html', title='Adding a manga', form=add_form)


def main():
    db_session.global_init("db/manga.sqlite")
    app.register_blueprint(news_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
