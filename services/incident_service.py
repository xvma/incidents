import os
import json
from flask import Flask, request, jsonify

from models.incident_model import Incident, IncidentStatus, IncidentSource, IncidentField
from db.database import Database
# __________________________________________________________________________

def create_service(db_path):
    app = Flask(__name__)
    db = Database(db_path)

    @app.route('/incidents/create', methods=['POST'])
    def create_incident():
        data = request.get_json()

        if not type(data) is dict:
            return jsonify({'error': 'Missing required data: incident'}), 400

        incident = Incident.from_dict(data)
        id = db.create_incident(incident)
        return jsonify({"id": id}), 201

    @app.route('/incidents', methods=['GET'])
    def get_incidents():
        status_param = request.args.get('status')

        if status_param:
            try:
                status = IncidentStatus(status_param)
            except ValueError:
                return jsonify({'error': 'Invalid status. Must be one of: new, ongoing, resolved, closed'}), 400
            incidents = db.get_incidents(status)
        else:
            incidents = db.get_incidents()

        return jsonify([incident.to_dict() for incident in incidents])

    @app.route('/incidents/<int:incident_id>/status', methods=['PATCH'])
    def update_incident_status(incident_id):
        data = request.get_json()

        if not data or 'status' not in data:
            return jsonify({'error': 'Missing required field: status'}), 400

        try:
            new_status = IncidentStatus(data['status'])
        except ValueError:
            return jsonify({'error': 'Invalid status. Must be one of: new, ongoing, resolved, closed'}), 400

        result = db.update_incident_status(incident_id, new_status)

        if result <= 0:
            return jsonify({'error': 'Incident not found'}), 404

        return '', 204

    @app.route('/incidents/<int:incident_id>', methods=['GET'])
    def get_incident(incident_id):
        incident = db.get_incident_by_id(incident_id)

        if not incident:
            return jsonify({'error': 'Incident not found'}), 404

        return jsonify(incident.to_dict())

    return app
