import flask
from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return flask.jsonify({
        'jobs': [item.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date',
                                    'is_finished')) for item in jobs]})


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return flask.make_response(flask.jsonify({'error': 'Job not found'}), 404)
    return flask.jsonify({
        'job': job.to_dict(only=('id', 'job', 'team_leader', 'work_size', 'collaborators', 'start_date', 'end_date',
                                 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)

    required_fields = ['job', 'team_leader', 'work_size', 'collaborators', 'is_finished']
    if not all(field in flask.request.json for field in required_fields):
        return flask.make_response(flask.jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    job = Jobs()
    job.job = flask.request.json['job']
    job.team_leader = flask.request.json['team_leader']
    job.work_size = flask.request.json['work_size']
    job.collaborators = flask.request.json['collaborators']
    job.is_finished = flask.request.json['is_finished']

    db_sess.add(job)
    db_sess.commit()

    return flask.jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return flask.make_response(flask.jsonify({'error': 'Job not found'}), 404)

    db_sess.delete(job)
    db_sess.commit()

    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['PUT'])
def edit_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return flask.make_response(flask.jsonify({'error': 'Job not found'}), 404)

    if not flask.request.json:
        return flask.make_response(flask.jsonify({'error': 'Empty request'}), 400)

    if 'job' in flask.request.json:
        job.job = flask.request.json['job']
    if 'team_leader' in flask.request.json:
        job.team_leader = flask.request.json['team_leader']
    if 'work_size' in flask.request.json:
        job.work_size = flask.request.json['work_size']
    if 'collaborators' in flask.request.json:
        job.collaborators = flask.request.json['collaborators']
    if 'is_finished' in flask.request.json:
        job.is_finished = flask.request.json['is_finished']

    db_sess.commit()

    return flask.jsonify({'success': 'OK'})