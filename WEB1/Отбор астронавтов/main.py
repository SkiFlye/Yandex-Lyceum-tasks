import os
from flask import Flask, request, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img/uploads'


@app.route('/')
def mission():
    return "Миссия Колонизация Марса"


@app.route('/index')
def motto():
    return "И на Марсе будут яблони цвести!"


@app.route('/promotion')
def promotion():
    lines = [
        "Человечество вырастает из детства.",
        "Человечеству мала одна планета.",
        "Мы сделаем обитаемыми безжизненные пока планеты.",
        "И начнем с Марса!",
        "Присоединяйся!"]
    return "</br>".join(lines)


@app.route('/image_mars')
def image_mars():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <title>Привет, Марс!</title>
                  </head>
                  <body>
                    <h1>Жди нас, Марс!</h1>
                    <img src="{url_for('static', filename='img/mars.png')}" alt="Марс">
                    <p>Вот она какая, красная планета!</p>
                  </body>
                </html>'''


@app.route('/promotion_image')
def promotion_image():
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}">
                    <title>Реклама Марса</title>
                  </head>
                  <body>
                    <div class="container">
                        <h1>Жди нас, Марс!</h1>
                        <img src="{url_for('static', filename='img/mars.png')}" alt="Марс">
                        <p>Вот она какая, красная планета!</p>
                        <div class="line1">Человечество вырастает из детства.</div>
                        <div class="line2">Человечеству мала одна планета.</div>
                        <div class="line3">Мы сделаем обитаемыми безжизненные пока планеты.</div>
                        <div class="line4">И начнем с Марса!</div>
                        <div class="line5">Присоединяйся!</div>
                    </div>
                  </body>
                </html>'''


@app.route('/astronaut_selection', methods=['GET', 'POST'])
def astronaut_selection():
    professions = [
        "инженер-исследователь", "пилот", "строитель", "экзобиолог", "врач",
        "инженер по терраформированию", "климатолог", "специалист по радиационной защите",
        "астрогеолог", "гляциолог", "инженер жизнеобеспечения", "метеоролог",
        "оператор марсохода", "киберинженер", "штурман", "пилот дронов"]
    profession_radios = ""
    for prof in professions:
        profession_radios += f'''
            <div>
                <input type="radio" id="{prof}" name="profession" value="{prof}">
                <label for="{prof}">{prof}</label>
            </div>
        '''
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Отбор астронавтов</title>
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}">
                  </head>
                  <body>
                    <h1>Анкета кандидата</h1>
                    <div class="form-container">
                        <form method="post">
                            <div class="form-group">
                                <label for="surname">Фамилия</label>
                                <input type="text" id="surname" name="surname">
                            </div>
                            <div class="form-group">
                                <label for="name">Имя</label>
                                <input type="text" id="name" name="name">
                            </div>
                            <div class="form-group">
                                <label for="email">Email</label>
                                <input type="email" id="email" name="email">
                            </div>
                            <div class="form-group">
                                <label for="education">Образование</label>
                                <select id="education" name="education">
                                    <option value="">Выберите образование</option>
                                    <option value="high_school">Среднее</option>
                                    <option value="bachelor">Высшее</option>
                                    <option value="phd">Учёная степень</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Профессия</label>
                                <div class="radio-group">
                                    {profession_radios}
                                </div>
                            </div>
                            <div class="form-group">
                                <label>Пол</label>
                                <div class="radio-group">
                                    <div>
                                        <input type="radio" id="male" name="gender" value="male">
                                        <label for="male">Мужской</label>
                                    </div>
                                    <div>
                                        <input type="radio" id="female" name="gender" value="female">
                                        <label for="female">Женский</label>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <label for="motivation">Мотивация</label>
                                <textarea id="motivation" name="motivation" rows="5"></textarea>
                            </div>
                            <div class="checkbox-group">
                                <input type="checkbox" id="stay" name="stay" value="yes">
                                <label for="stay">Готов(а) остаться на Марсе навсегда</label>
                            </div>
                            <button type="submit">Отправить</button>
                        </form>
                    </div>
                  </body>
                </html>'''


@app.route('/choice/<planet_name>')
def choice(planet_name):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Ваш выбор</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                  </head>
                  <body>
                    <div class="container mt-4">
                        <h1>Моё предложение: {planet_name}</h1>
                        <h2 class="mt-3">Эта планета близка к Земле;</h2>
                        <div class="alert alert-success mt-3" role="alert">
                            <h3>На ней много необходимых ресурсов;</h3>
                        </div>
                        <div class="alert alert-info" role="alert">
                            <h4>На ней есть вода и атмосфера;</h4>
                        </div>
                        <div class="alert alert-warning" role="alert">
                            <h5>На ней есть небольшое магнитное поле;</h5>
                        </div>
                        <div class="alert alert-danger" role="alert">
                            <h6>Наконец, она просто красива!</h6>
                        </div>
                    </div>
                  </body>
                </html>'''


@app.route('/results/<nickname>/<int:level>/<float:rating>')
def results(nickname, level, rating):
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Результаты отбора</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                  </head>
                  <body>
                    <div class="container mt-4">
                        <h1>Результаты отбора</h1>
                        <h2>Претендента на участие в миссии {nickname}:</h2>
                        <div class="alert alert-success mt-3" role="alert">
                            Поздравляем! Ваш рейтинг после {level} этапа отбора 
                        </div>
                        составляет {rating}!
                        <div class="alert alert-warning" role="alert">
                            Желаем удачи!
                        </div>
                    </div>
                  </body>
                </html>'''


@app.route('/load_photo', methods=['GET', 'POST'])
def load_photo():
    if not os.path.exists('static/img/uploads'):
        os.makedirs('static/img/uploads')
    uploaded_files = []
    if os.path.exists('static/img/uploads'):
        uploaded_files = os.listdir('static/img/uploads')
    photo_url = url_for('static', filename='img/mars.png')
    if uploaded_files:
        latest_file = uploaded_files[0]
        photo_url = url_for('static', filename=f'img/uploads/{latest_file}')
    if request.method == 'POST':
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                for file in uploaded_files:
                    file_path = os.path.join('static/img/uploads', file)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                filename = photo.filename
                photo.save(os.path.join('static/img/uploads', filename))
                photo_url = url_for('static', filename=f'img/uploads/{filename}')
    return f'''<!doctype html>
                <html lang="en">
                  <head>
                    <meta charset="utf-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <title>Загрузка фотографии</title>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css">
                    <link rel="stylesheet" type="text/css" href="{url_for('static', filename='css/style.css')}">
                  </head>
                  <body>
                    <h1>Загрузка фотографии для участия в миссии</h1>
                    <div class="form-container">
                        <form method="post" enctype="multipart/form-data">
                            <div class="form-group">
                                <label for="photo">Приложите фотографию</label>
                                <input type="file" id="photo" name="photo" accept="image/*">
                            </div>
                            <button type="submit">Отправить</button>
                        </form>
                        <div class="photo-preview">
                            <img src="{photo_url}" alt="Фото" style="max-width: 300px; max-height: 300px; border: 2px solid #ddd; border-radius: 8px;">
                        </div>
                    </div>
                  </body>
                </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')