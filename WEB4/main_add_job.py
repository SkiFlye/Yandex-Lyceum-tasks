from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.jobs import Jobs
from data.users import User
from data.departments import Department
from data.login_form import LoginForm
from data.add_job import AddJobForm
from data.register import RegisterForm
from data.department_form import DepartmentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


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
                               message="Wrong login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="User already exists")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def addjob():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.team_leader = current_user.id
        job.work_size = int(form.work_size.data)
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Adding a Job', form=form)


@app.route('/edit_job/<int:job_id>', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    form = AddJobForm()
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return render_template('error.html', message='Job not found')
    if current_user.id != 1 and job.team_leader != current_user.id:
        return render_template('error.html', message='You do not have permission to edit this job')
    if form.validate_on_submit():
        job.job = form.job.data
        job.work_size = int(form.work_size.data)
        job.collaborators = form.collaborators.data
        job.is_finished = form.is_finished.data
        db_sess.commit()
        return redirect('/')
    form.job.data = job.job
    form.work_size.data = job.work_size
    form.collaborators.data = job.collaborators
    form.is_finished.data = job.is_finished
    return render_template('addjob.html', title='Editing a Job', form=form)


@app.route('/delete_job/<int:job_id>', methods=['GET'])
@login_required
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return render_template('error.html', message='Job not found')
    if current_user.id != 1 and job.team_leader != current_user.id:
        return render_template('error.html', message='You do not have permission to delete this job')
    db_sess.delete(job)
    db_sess.commit()
    return redirect('/')


@app.route('/departments')
def departments():
    db_sess = db_session.create_session()
    departments = db_sess.query(Department).all()
    users = db_sess.query(User).all()
    names = {user.id: (user.surname, user.name) for user in users}
    return render_template("departments.html", departments=departments, names=names, title='Departments log')


@app.route('/add_department', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        department = Department()
        department.title = form.title.data
        department.chief = current_user.id
        department.members = form.members.data
        department.email = form.email.data
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('department_form.html', title='Adding a Department', form=form)


@app.route('/edit_department/<int:department_id>', methods=['GET', 'POST'])
@login_required
def edit_department(department_id):
    form = DepartmentForm()
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id).first()
    if not department:
        return render_template('error.html', message='Department not found')
    if current_user.id != 1 and department.chief != current_user.id:
        return render_template('error.html', message='You do not have permission to edit this department')
    if form.validate_on_submit():
        department.title = form.title.data
        department.members = form.members.data
        department.email = form.email.data
        db_sess.commit()
        return redirect('/departments')
    form.title.data = department.title
    form.members.data = department.members
    form.email.data = department.email
    return render_template('department_form.html', title='Editing a Department', form=form)


@app.route('/delete_department/<int:department_id>', methods=['GET'])
@login_required
def delete_department(department_id):
    db_sess = db_session.create_session()
    department = db_sess.query(Department).filter(Department.id == department_id).first()
    if not department:
        return render_template('error.html', message='Department not found')
    if current_user.id != 1 and department.chief != current_user.id:
        return render_template('error.html', message='You do not have permission to delete this department')
    db_sess.delete(department)
    db_sess.commit()
    return redirect('/departments')


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {user.id: (user.surname, user.name) for user in users}
    return render_template("index.html", jobs=jobs, names=names, title='Work log')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()