from flask import render_template, redirect, Flask, request, make_response, jsonify, url_for
from flask_login import LoginManager, login_user, current_user
from data import db_session, jobs_api, users_api
from data.departments import Department
from data.map import get_city_map
from data.users import User
from data.jobs import Job
from data.category import Category
from forms.add_department import DepartAdditionForm
from forms.add_job import JobAdditionForm
from forms.user_forms import LoginForm, RegisterForm
from requests import get

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route("/")
@app.route('/works_log')
def work_log():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    if current_user.is_authenticated:
        editable_jobs = db_sess.query(Job).filter((Job.team_leader == current_user.id) | (current_user.id == 1))
    else:
        editable_jobs = []
    return render_template('jobs_list.html', jobs=jobs, current_user=current_user, editable_jobs=editable_jobs)


@app.route('/departments_log')
def departments_log():
    db_sess = db_session.create_session()
    departs = db_sess.query(Department).all()
    if current_user.is_authenticated:
        editable_departs = db_sess.query(Department).filter((Department.chief == current_user.id)
                                                            | (current_user.id == 1))
    else:
        editable_departs = []
    return render_template('departments_list.html', departs=departs, current_user=current_user,
                           editable_departs=editable_departs)


@app.route("/register", methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobAdditionForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if not current_user.is_authenticated:
            return render_template('add_job.html', title='Добавление работ',
                                   form=form,
                                   message="Авторизируйтесь чтобы добавить работу")
        if db_sess.query(Job).filter(Job.job == form.job.data).first():
            return render_template('add_job.html', title='Добавление работ',
                                   form=form,
                                   message="Такая работа уже есть")
        job = Job(
            team_leader=form.teamleader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
        )
        for category in form.categories.data.split(','):
            job.categories.append(db_sess.query(Category).filter(Category.id == category).first())
        db_sess.add(job)
        db_sess.commit()
        return redirect('/works_log')
    return render_template('add_job.html', title='Добавление работ', form=form)


@app.route('/change_job/<id>', methods=['GET', 'POST'])
def change_job(id):
    form = JobAdditionForm()
    db_sess = db_session.create_session()
    selected_job = db_sess.query(Job).filter(Job.id == id).first()
    if request.method == 'GET':
        form.teamleader.data = selected_job.team_leader
        form.job.data = selected_job.job
        form.work_size.data = selected_job.work_size
        form.collaborators.data = selected_job.collaborators
        form.is_finished.data = selected_job.is_finished
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return render_template('add_job.html',
                                   title='Изменение работ',
                                   form=form,
                                   message="Авторизируйтесь, чтобы изменить работу")
        if current_user.id != selected_job.team_leader and current_user.id != 1:
            return render_template('add_job.html',
                                   title='Изменение работ',
                                   form=form,
                                   message="Недостаточно прав")
        selected_job = db_sess.query(Job).filter(Job.id == id).first()
        selected_job.team_leader = form.teamleader.data
        selected_job.job = form.job.data
        selected_job.work_size = form.work_size.data
        selected_job.collaborators = form.collaborators.data
        selected_job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/works_log')
    return render_template('add_job.html', title='Изменение работ',
                           form=form)


@app.route('/delete_job/<id>', methods=['GET', 'POST'])
def delete_job(id):
    form = JobAdditionForm()
    db_sess = db_session.create_session()
    selected_job = db_sess.query(Job).filter(Job.id == id).first()
    if request.method == 'GET':
        form.teamleader.data = selected_job.team_leader
        form.job.data = selected_job.job
        form.work_size.data = selected_job.work_size
        form.collaborators.data = selected_job.collaborators
        form.is_finished.data = selected_job.is_finished
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return render_template('add_job.html',
                                   title=''
                                         'Удаление работ',
                                   form=form,
                                   message="Авторизируйтесь, чтобы удалить работу")
        if current_user.id != selected_job.team_leader and current_user.id != 1:
            return render_template('add_job.html',
                                   title='Удаление работ',
                                   form=form,
                                   message="Недостаточно прав")
        db_sess.query(Job).filter(Job.id == id).delete()
        db_sess.commit()
        return redirect('/works_log')
    return render_template('add_job.html', title='Удаление работ',
                           form=form)


@app.route('/add_depart', methods=['GET', 'POST'])
def add_depart():
    form = DepartAdditionForm()
    if not current_user.is_authenticated:
        return render_template('add_department.html', title='Добавление департаментов',
                               form=form,
                               message="Авторизируйтесь чтобы добавить департамент")
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = Department(
            title=form.title.data,
            chief=form.chief.data,
            members=form.members.data,
            email=form.email.data,
        )
        db_sess.add(depart)
        db_sess.commit()
        return redirect('/departments_log')
    return render_template('add_department.html', title='Добавление департаментов', form=form)


@app.route('/change_depart/<id>', methods=['GET', 'POST'])
def change_depart(id):
    form = DepartAdditionForm()
    db_sess = db_session.create_session()
    selected_depart = db_sess.query(Department).filter(Department.id == id).first()
    if request.method == 'GET':
        form.title.data = selected_depart.title
        form.chief.data = selected_depart.chief
        form.members.data = selected_depart.members
        form.email.data = selected_depart.email

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            return render_template('add_department.html',
                                   title='Добавление работ',
                                   form=form,
                                   message="Авторизируйтесь чтобы изменить департамент")
        if current_user.id != selected_depart.chief and current_user.id != 1:
            return render_template('add_department.html',
                                   title='Добавление работ',
                                   form=form,
                                   message="Недостаточно прав")
        db_sess = db_session.create_session()
        selected_depart = db_sess.query(Department).filter(Department.id == id).first()
        selected_depart.title = form.title.data
        selected_depart.chief = form.chief.data
        selected_depart.members = form.members.data
        selected_depart.email = form.email.data
        db_sess.commit()
        return redirect('/departments_log')
    return render_template('add_department.html', title='Добавление департаментов',
                           form=form)


@app.route('/delete_depart/<id>')
def delete_depart(id):
    db_sess = db_session.create_session()
    db_sess.query(Department).filter(Department.id == id).delete()
    db_sess.commit()
    return redirect('/departments_log')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/users_show/<int:user_id>')
def users_show(user_id):
    response = get(f'http://127.0.0.1:8080/api/users/{user_id}')
    if not response:
        return "User is not found"
    user = response.json()['users'][0]
    city = user['city_from']
    name = user['name']
    city_img = get_city_map(city)
    with open('static/img/city.png', "wb") as file:
        file.write(city_img)
    url = url_for('static', filename='img/city.png')
    return render_template('show_map.html', city=city, name=name, url=url)


if __name__ == '__main__':
    db_session.global_init("db/mars.db")
    app.register_blueprint(jobs_api.blueprint)
    app.register_blueprint(users_api.blueprint)
    app.run(port=8080, host='127.0.0.1')
