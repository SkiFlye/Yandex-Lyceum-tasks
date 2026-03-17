from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, help="surname cannot be blank")
parser.add_argument('name', required=True, help="name cannot be blank")
parser.add_argument('age', required=True, type=int, help="age cannot be blank")
parser.add_argument('position', required=True, help="position cannot be blank")
parser.add_argument('speciality', required=True, help="speciality cannot be blank")
parser.add_argument('address', required=True, help="address cannot be blank")
parser.add_argument('email', required=True, help="email cannot be blank")
parser.add_argument('password', required=True, help="password cannot be blank")
parser.add_argument('city_from', required=False)