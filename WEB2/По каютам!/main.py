from flask import Flask, render_template, redirect
from forms import EmergencyAccessForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route('/')
def index_root():
    return render_template('base.html', title='Главная')

@app.route('/index/<title>')
def index_title(title):
    return render_template('base.html', title=title)

@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', title='Тренировки', prof=prof)

@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    professions = ['инженер', 'пилот', 'строитель', 'биолог', 'врач']
    return render_template('list_prof.html',
                         title='Список профессий',
                         professions=professions,
                         list_type=list_type)

@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    user_data = {
        'title': 'Анкета',
        'surname': 'Иванов',
        'name': 'Иван',
        'education': 'высшее',
        'profession': 'инженер',
        'sex': 'мужской',
        'motivation': 'Хочу колонизировать Марс',
        'ready': 'true'
    }
    return render_template('auto_answer.html', **user_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = EmergencyAccessForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html',
                         title='Аварийный доступ',
                         form=form)

@app.route('/success')
def success():
    return "Доступ предоставлен"

@app.route('/distribution')
def distribution():
    astronauts = ['Ридли Скотт', 'Энди Уир', 'Марк Уотни', 'Венката Капур', 'Тедди Сандрес', 'Шон Бин']
    return render_template('distribution.html',
                         title='Размещение по каютам',
                         astronauts=astronauts)

if __name__ == '__main__':
    app.run(port=8080)