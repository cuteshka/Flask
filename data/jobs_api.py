import flask
from flask import jsonify, make_response, request

from . import db_session
from .category import Category
from .jobs import Job

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Job).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id',
                                    'team_leader',
                                    'leader.name',
                                    'leader.surname',
                                    'job',
                                    'work_size',
                                    'collaborators',
                                    'start_date',
                                    'end_date',
                                    'is_finished',
                                    ))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Job).filter(Job.id == job_id).first()
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs':
                job.to_dict(
                    only=(
                        'id',
                        'team_leader',
                        'leader.name',
                        'leader.surname',
                        'job',
                        'work_size',
                        'collaborators',
                        'start_date',
                        'end_date',
                        'is_finished',
                    )
                )
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def add_job():
    req_json = request.get_json()
    if not req_json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    required_keys = ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished', 'categories']
    if not all(key in req_json for key in required_keys):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    if not (isinstance(req_json['team_leader'], int) and
            isinstance(req_json['job'], str) and
            isinstance(req_json['work_size'], int) and
            isinstance(req_json['collaborators'], str) and
            isinstance(req_json['is_finished'], bool) and
            isinstance(req_json['categories'], str)):  # categories ожидает строку
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()
    job = Job(
        team_leader=req_json['team_leader'],
        job=req_json['job'],
        work_size=req_json['work_size'],
        collaborators=req_json['collaborators'],
        is_finished=req_json['is_finished'],
    )
    for category in request.json['categories'].split(','):
        category_item = db_sess.query(Category).filter(Category.id == category).first()
        if not category_item:
            return make_response(jsonify({'error': 'Not found'}), 404)
        job.categories.append(category_item)
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})
