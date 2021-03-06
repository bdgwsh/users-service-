from flask import jsonify, request, Response
from sqlalchemy import exc
from database.models import User
from database.db import db
from app import app


@app.route('/users/', methods=['GET'])
def get_users():
    users_list = list()
    users = User.query.all()
    for user in users:
        users_list.append({"id": user.id, "login": user.login})
    return jsonify({"users": users_list})


@app.route('/users/', methods=['POST'])
def add_user():
    try:
        new_user = User(
            login=request.json['login'],
            password=request.json['password'])
        db.session.add(new_user)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return Response(status=400)
    return jsonify({"id": new_user.id})


@app.route('/users/<int:user_id>', methods=['PATCH'])
def change_password(user_id):
    if User.query.filter_by(id=user_id).update(
            {'password': request.json['password']}):
        db.session.commit()
        return jsonify({"id": user_id})
    else:
        db.session.rollback()
        return Response(status=400)


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"id": user.id})
    else:
        return Response(status=400)


@app.route('/auth/', methods=['POST'])
def check_user():
    user = User.query.filter_by(login=request.json['login']).first()
    if user and user.password == request.json['password']:
        return Response(status=200)
    else:
        return Response(status=401)
