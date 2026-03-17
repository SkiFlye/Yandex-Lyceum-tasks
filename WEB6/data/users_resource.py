import flask
from flask_restful import abort, Resource
from data.db_session import create_session
from data.users import User
from data.users_parser import parser


def abort_if_user_not_found(user_id):
    session = create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        return flask.jsonify({'user': user.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality',
                                                         'address', 'email', 'city_from'))})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return flask.jsonify({'success': 'OK'})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        session = create_session()
        user = session.query(User).get(user_id)
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        if args.get('city_from'):
            user.city_from = args['city_from']
        user.set_password(args['password'])
        session.commit()
        return flask.jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = create_session()
        users = session.query(User).all()
        return flask.jsonify({'users': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'position',
                  'speciality', 'address', 'email', 'city_from'))
            for item in users]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        if session.query(User).filter(User.email == args['email']).first():
            abort(400, message="Email already exists")
        user = User()
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.position = args['position']
        user.speciality = args['speciality']
        user.address = args['address']
        user.email = args['email']
        if args.get('city_from'):
            user.city_from = args['city_from']
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return flask.jsonify({'id': user.id})