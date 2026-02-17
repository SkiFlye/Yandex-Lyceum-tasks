from flask import Flask, url_for

app = Flask(__name__)


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
        "Присоединяйся!"
    ]
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
                        <div class="line1">Человечество вырастает из детства.</div>
                        <div class="line2">Человечеству мала одна планета.</div>
                        <div class="line3">Мы сделаем обитаемыми безжизненные пока планеты.</div>
                        <div class="line4">И начнем с Марса!</div>
                        <div class="line5">Присоединяйся!</div>
                    </div>
                  </body>
                </html>'''


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')