import flask
from flask_login import current_user
from data import db_session
from data.users import User

blueprint = flask.Blueprint('users_api', __name__, template_folder='templates')


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return flask.jsonify({
        'users': [item.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                     'speciality', 'address', 'email', 'city_from'))
                  for item in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'error': 'User not found'}), 404)
    return flask.jsonify({
        'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position',
                                   'speciality', 'address', 'email', 'city_from'))})


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)

    required_fields = ['surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'password']
    if not all(field in flask.request.json for field in required_fields):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()

    if db_sess.query(User).filter(User.email == flask.request.json['email']).first():
        return flask.make_response(flask.jsonify({'error': 'Email already exists'}), 400)

    user = User()
    user.surname = flask.request.json['surname']
    user.name = flask.request.json['name']
    user.age = flask.request.json['age']
    user.position = flask.request.json['position']
    user.speciality = flask.request.json['speciality']
    user.address = flask.request.json['address']
    user.email = flask.request.json['email']
    user.city_from = flask.request.json.get('city_from', '')
    user.set_password(flask.request.json['password'])

    db_sess.add(user)
    db_sess.commit()

    return flask.jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'error': 'User not found'}), 404)

    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)

    if 'surname' in flask.request.json:
        user.surname = flask.request.json['surname']
    if 'name' in flask.request.json:
        user.name = flask.request.json['name']
    if 'age' in flask.request.json:
        user.age = flask.request.json['age']
    if 'position' in flask.request.json:
        user.position = flask.request.json['position']
    if 'speciality' in flask.request.json:
        user.speciality = flask.request.json['speciality']
    if 'address' in flask.request.json:
        user.address = flask.request.json['address']
    if 'city_from' in flask.request.json:
        user.city_from = flask.request.json['city_from']
    if 'email' in flask.request.json:
        if flask.request.json['email'] != user.email:
            if db_sess.query(User).filter(User.email == flask.request.json['email']).first():
                return flask.make_response(flask.jsonify({'error': 'Email already exists'}), 400)
        user.email = flask.request.json['email']
    if 'password' in flask.request.json:
        user.set_password(flask.request.json['password'])

    db_sess.commit()

    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.make_response(flask.jsonify({'error': 'User not found'}), 404)

    db_sess.delete(user)
    db_sess.commit()

    return flask.jsonify({'success': 'OK'})


@blueprint.route('/users_show/<int:user_id>', methods=['GET'])
def show_user_city(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return "Пользователь не найден", 404
    return flask.render_template('user_city.html', user=user, current_user=current_user)