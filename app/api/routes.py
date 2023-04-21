from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, Storm, storm_schema, storms_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/storms', methods=['POST'])
@token_required
def add_storm(current_user_token):
    type_storm = request.json['type_storm']
    severity = request.json['severity']
    date_happened = request.json['data_happened']
    damage_cost = request.json['damage_cost']
    user_token = current_user_token.token

    storm = Storm(type_storm=type_storm, severity=severity, user_token=user_token, date_happened=date_happened, damage_cost=damage_cost)

    db.session.add(storm)
    db.session.commit()

    response = storm_schema.dump(storm)
    return jsonify(response)


@api.route('/storms', methods = ['GET'])
@token_required
def get_all_storms(current_user_token):
    a_user = current_user_token.token
    storms = Storm.query.filter_by(user_token = a_user).all()

    response = storms_schema.dump(storms)
    return jsonify(response)

@api.route('/storms/<id>', methods = ['GET'])
@token_required
def get_single_storm(current_user_token, id):
    storm = Storm.query.get(id)

    response = storm_schema.dump(storm)
    return jsonify(response)

@api.route('/storm/<id>', methods = ['POST', 'PUT'])
@token_required
def update_image_info(current_user_token, id):
    storm = Storm.query.get(id)
    storm.type_storm = request.json['type_storm']
    storm.severity = request.json['severity']
    storm.date_happened = request.json['date_happened']
    storm.damage_cost = request.json['damage_cost']
    storm.user_token = current_user_token.token

    db.session.commit()

    response = storm_schema.dump(storm)
    return jsonify(response)

@api.route('/storms/<id>', methods = ['DELETE'])
@token_required
def delete_storm(current_user_token, id):
    storm = Storm.query.get(id)

    db.session.delete(storm)
    db.session.commit()

    response = storm_schema.dump(storm)
    return jsonify(response)