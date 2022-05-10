import flask
from flask import jsonify, request
from data import db_session
from data.jobs import Jobs
import json
import datetime

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'team_leader', 'user.name'))
                 for item in job]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_newss(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    else:
        return jsonify(
            {
                'jobs':
                    [job.to_dict(only=('job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'team_leader', 'user.name'))]
            }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['job', 'work_size', 'collaborators', 'start_date', 'end_date', 'is_finished', 'team_leader', 'user.name', 'id']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    if db_sess.query(Jobs).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    st = request.json['start_date']
    start = datetime.datetime.strptime(str(st), '%Y-%m-%d %H:%M:%S.%f')
    en = request.json['end_date']
    end = datetime.datetime.strptime(str(en), '%Y-%m-%d %H:%M:%S.%f')
    jobs = Jobs(
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=start,
        end_date=end,
        is_finished=request.json['is_finished'],
        team_leader=request.json['team_leader'],
        id=request.json['id']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})