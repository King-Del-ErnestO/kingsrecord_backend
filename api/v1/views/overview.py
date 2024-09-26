from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from database.db import KingsRecordDatabase
from datetime import datetime


storage = KingsRecordDatabase()

@app_look.route('/get-overview', methods=['GET'])
@jwt_required()
def handle_overview():
    """Handles overview request"""
    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    kwargs = {
        'year': data.get('year'),
        'category': data.get('category'),
        'count': data.get('count')
    }
    if not kwargs['year'] or not kwargs['category'] or not kwargs['count']:
        return jsonify({'error': 'All fields are required'}), 400