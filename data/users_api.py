import flask
import datetime

from . import db_session
from .users import User
from flask import jsonify, make_response, request

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(
                    only=(
                        'id',
                        'surname',
                        'name',
                        'age',
                        'position',
                        'speciality',
                        'address',
                        'city_from',
                        'email',
                        'modified_date'
                    )
                )
                    for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users':
                [
                    user.to_dict(
                        only=(
                            'id',
                            'surname',
                            'name',
                            'age',
                            'position',
                            'speciality',
                            'address',
                            'city_from',
                            'email',
                            'modified_date'
                        )
                    )
                ]
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def add_users():
    req_json = request.json
    if not req_json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in req_json for key in
                 ['surname', 'name', 'age', 'position',
                  'speciality', 'address', 'city_from', 'email']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    try:
        db_sess = db_session.create_session()
        user = User(
            surname=req_json['surname'],
            name=req_json['name'],
            age=req_json['age'],
            position=req_json['position'],
            speciality=req_json['speciality'],
            address=req_json['address'],
            city_from=req_json['city_from'],
            email=req_json['email']
        )
        db_sess.add(user)
        db_sess.commit()
    except Exception:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def put_user(user_id):
    req_json = request.json
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    user.surname = req_json.get('surname', user.surname)
    user.name = req_json.get('name', user.name)
    user.age = req_json.get('age', user.age)
    user.position = req_json.get('position', user.position)
    user.speciality = req_json.get('speciality', user.speciality)
    user.address = req_json.get('address', user.address)
    user.email = req_json.get('email', user.email)
    user.city_from = req_json.get('city_from', user.city_from)
    user.modified_date = datetime.datetime.now()

    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})
