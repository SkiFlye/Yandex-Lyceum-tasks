from flask import Flask, render_template

app = Flask(__name__)

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
    professions = [
        'Инженер-конструктор',
        'Пилот',
        'Строитель',
        'Биолог',
        'Врач',
        'Геолог',
        'Астрофизик',
        'Программист',
        'Специалист по жизнеобеспечению',
        'Механик',
        'Психолог']
    return render_template('list_prof.html',
                         title='Список профессий',
                         professions=professions,
                         list_type=list_type)

if __name__ == '__main__':
    app.run(port=8080)