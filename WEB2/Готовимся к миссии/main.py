from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index_root():
    return render_template('base.html', title='Главная')


@app.route('/index/<title>')
def index_title(title):
    return render_template('base.html', title=title)


if __name__ == '__main__':
    app.run(port=8080)

