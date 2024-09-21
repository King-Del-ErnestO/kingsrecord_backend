from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from database.db import KingsRecordDatabase
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, get_jwt_identity, \
    jwt_required

storage = KingsRecordDatabase()

@app_look.route('/admin-register', methods=['POST'])
def reg_admin():
    """Registers a new admin account"""
    kwargs = {
        'title': request.form.get('title'),
        'firstName': request.form.get('firstName'),
        'lastName': request.form.get('lastName'),
        'email': request.form.get('email'),
        'password': request.form.get('password'),
        'chapter': request.form.get('chapter'),
        'phoneNumber': request.form.get('phoneNumber')
    }

    if not kwargs['email'] or not kwargs['password'] or not kwargs['title'] or not kwargs['firstName'] \
    or not kwargs['lastName'] or not kwargs['chapter'] or not kwargs['phoneNumber']:
        return jsonify({'error': 'All fields are required'}), 400
    print(kwargs['password'])
    chkMail = storage.get_admin_by_email(kwargs['email'])
    if chkMail:
        return jsonify({'error': 'Email already exists'}), 400
    print(f'User registration data: {kwargs}')
    user = storage.reg_admin_user(**kwargs)
    if user is None:
        return jsonify({'error': 'Failed to create user'}), 500 
    print(user.password, user.email)
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'message': 'Admin account created successfully', 'access_token': access_token}), 201

@app_look.route('/admin-login', methods=['POST'])
def login_admin():
    """Logs in admin"""
    email = request.form.get('email')
    password = request.form.get('password')
    print(email, password)
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    user = storage.get_admin_by_email(email)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    if not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 401
    access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
    return jsonify({'message': 'Logged in successfully', 'access_token': access_token}), 200