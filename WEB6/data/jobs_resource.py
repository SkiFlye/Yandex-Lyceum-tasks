import flask
from flask_restful import abort, Resource
from data.db_session import create_session
from data.jobs import Jobs
from data.jobs_parser import parser


def abort_if_job_not_found(job_id):
    session = create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = create_session()
        job = session.query(Jobs).get(job_id)
        return flask.jsonify({'job': job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators',
                                                       'start_date', 'end_date', 'is_finished', 'category'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = create_session()
        job = session.query(Jobs).get(job_id)
        session.delete(job)
        session.commit()
        return flask.jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = create_session()
        jobs = session.query(Jobs).all()
        return flask.jsonify({'jobs': [item.to_dict(
            only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished',
                  'category'))
            for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = create_session()
        job = Jobs()
        job.job = args['job']
        job.team_leader = args['team_leader']
        job.work_size = args['work_size']
        job.collaborators = args['collaborators']
        job.is_finished = args['is_finished']
        if args.get('category'):
            job.category = args['category']
        session.add(job)
        session.commit()
        return flask.jsonify({'id': job.id})