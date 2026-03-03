import os
from flask import Flask, render_template
from data import db_session
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template("index.html", jobs=jobs)


def main():
    db_file = "db/mars_explorer.db"
    db_dir = os.path.dirname(db_file)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    db_session.global_init(db_file)
    app.run()


if __name__ == '__main__':
    main()