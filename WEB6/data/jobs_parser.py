from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('job', required=True, help="job description cannot be blank")
parser.add_argument('team_leader', required=True, type=int, help="team leader id cannot be blank")
parser.add_argument('work_size', required=True, type=int, help="work size cannot be blank")
parser.add_argument('collaborators', required=True, help="collaborators cannot be blank")
parser.add_argument('is_finished', required=True, type=bool, help="is_finished cannot be blank")
parser.add_argument('category', required=False)