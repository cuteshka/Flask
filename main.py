from flask import render_template, redirect, Flask, request
from flask_login import LoginManager, login_user, current_user
from data import db_session
from data.users import User
from data.jobs import Job
from forms.add_job import JobAdditionForm
from forms.user_forms import LoginForm, RegisterForm

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


if __name__ == '__main__':
    db_session.global_init("db/mars.db")
    app.run(port=8080, host='127.0.0.1')
