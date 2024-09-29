from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from database.db import KingsRecordDatabase
from datetime import datetime

storage = KingsRecordDatabase()


@app_look.route('/partnership-register', methods=['POST'])
@jwt_required()
def add_partnership():
    """Registers a new partnership"""
    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        data = request.json
        kwargs = {
            'title': data.get('title'),
            'firstName': data.get('firstName'),
            'lastName': data.get('lastName'),
            'email': data.get('email'),
            'phoneNumber': data.get('phoneNumber'),
            'admin': admin_id 
        }
        partnerships = data.get('partnerships', [])
        Date = data.get('Date')

        if not kwargs['firstName'] or not kwargs['lastName'] or not kwargs['Date'] \
        or not kwargs['email'] or not kwargs['phoneNumber']:
            return jsonify({'error': 'All fields are required'}), 400
        if not partnerships :
            return jsonify({'error': 'Partnership is required'}), 400

        email = kwargs['email']
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        chk_user = storage.get_user_by_email(email)
        if chk_user:
            if partnerships:
                for partner in partnerships:
                    if 'type' not in partner or 'amount' not in partner:
                        return jsonify({'error': 'Invalid partnership format'}), 400
                    type_details, amount = partner['type'], partner['amount']
                    existing_partnership = next((p for p in chk_user.partnership if p.type == type_details), None)
                    if existing_partnership:
                        existing_partnership.amount += amount
                        existing_partnership.updatedAt = datetime.now()
                    else:
                        chk_user.add_partnership(type_details, amount, Date, createdAt=datetime.now())
            chk_user.save()
            return jsonify({'message': 'Partnership added successfully'}), 201
        else:
            return jsonify({'error': 'Member not found in database'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app_look.route('/givings-register', methods=['POST'])
@jwt_required()
def add_givings():
    """Registers a new partnership"""
    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        data = request.json
        kwargs = {
            'title': data.get('title'),
            'firstName': data.get('firstName'),
            'lastName': data.get('lastName'),
            'email': data.get('email'),
            'phoneNumber': data.get('phoneNumber'),
            'admin': admin_id 
        }
        givings = data.get('givings', [])
        Date = data.get('Date')

        if not kwargs['firstName'] or not kwargs['lastName'] or not kwargs['Date'] \
        or not kwargs['email'] or not kwargs['phoneNumber']:
            return jsonify({'error': 'All fields are required'}), 400
        if not givings :
            return jsonify({'error': 'Partnership is required'}), 400

        email = kwargs['email']
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        chk_user = storage.get_user_by_email(email)
        if chk_user:
            if givings:
                for partner in givings:
                    if 'type' not in partner or 'amount' not in partner:
                        return jsonify({'error': 'Invalid partnership format'}), 400
                    type_details, amount = partner['type'], partner['amount']
                    existing_givings = next((p for p in chk_user.givings if p.type == type_details), None)
                    if existing_givings:
                        existing_givings.amount += amount
                        existing_givings.updatedAt = datetime.now()
                    else:
                        chk_user.add_giving(type_details, amount, Date, createdAt=datetime.now())
            chk_user.save()
            return jsonify({'message': 'Givings added successfully'}), 201
        else:
            return jsonify({'error': 'Member not found in database'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app_look.route('/add-member', methods=['POST'])
@jwt_required()
def add_member():
    """Registers a new user"""
    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    kwargs = {
        'title': data.get('title'),
        'firstName': data.get('firstName'),
        'lastName': data.get('lastName'),
        'email': data.get('email'),
        'birthDate': data.get('birthDate'),
        'phoneNumber': data.get('phoneNumber'),
        'church': data.get('church'),
        'cell': data.get('cell'),
        'admin': admin_id 
    }
    if  not kwargs['firstName'] or not kwargs['lastName'] or not kwargs['birthDate']  or not kwargs['email']\
    or not kwargs['phoneNumber']:
        return jsonify({'error': 'Required Fields are missing'}), 400
    user = storage.get_user_by_email(kwargs['email'])
    if user:
        return jsonify({'error': 'User is already in the database'}), 400
    new_user = storage.reg_user(**kwargs)
    if new_user is None:
        return jsonify({'error': 'User registration failed'}), 500
    return jsonify({'message': 'This member is added to the database'}), 201


@app_look.route('/spreadsheet', methods=['GET'])
@jwt_required()
def get_form_data():
    """Returns all form data"""
    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    month = request.args.get('month', None)
    year = request.args.get('year', None)

    users = storage.get_admin_users(admin_id)
    if not users:
        return jsonify({'message': 'No form data found'}), 200
    data = []
    total_partnership_sum = 0
    total_givings_sum = 0
    for user in users:
        partnership_total = 0
        givings_total = 0
        for p in user.partnership:
            try:
                date_obj = datetime.strptime(p.Date, '%Y-%m-%d')
            except ValueError:
                continue
            if (month and date_obj.month != int(month)) or (year and date_obj.year != int(year)):
                continue
            partnership_total += p.amount
        
        for g in user.givings:
            try:
                date_obj = datetime.strptime(g.Date, '%Y-%m-%d')
            except ValueError:
                continue
            if (month and date_obj.month != int(month)) or (year and date_obj.year != int(year)):
                continue
            givings_total += g.amount

        total_partnership_sum += partnership_total
        total_givings_sum += givings_total
        total_amount = partnership_total + givings_total

        user_dict = {
            'title': user.title,
            'firstName': user.firstName,
            'lastName': user.lastName,
            'Date': user.Date,
            'email': user.email,
            'phoneNumber': user.phoneNumber,
            'partnerships': [{'type': p.type, 'amount': p.amount, 'Date': p.Date} for p in user.partnership],
            'givings': [{'type': g.type, 'amount': g.amount, 'Date': g.Date} for g in user.givings],
            # 'totalPartnership': partnership_total,
            # 'totalGivings': givings_total,
            'total': total_amount
        }
        data.append(user_dict)
    return jsonify({'data': data}), 200

@app_look.route('/partnership-yearly/<year>', methods=['GET'])
@jwt_required()
def get_total_partnership_yearly(year):
    """Returns the total partnership for a given year"""

    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = storage.get_admin_users(admin_id)
    if not users:
        return jsonify({'message': 'No form data found'}), 401
    total_partnership_sum = 0
    for user in users:
        partnership_total = 0
        for p in user.partnership:
            try:
                date_obj = datetime.strptime(p.Date, '%Y-%m-%d')
            except ValueError:
                continue
            if date_obj.year != int(year):
                continue
            partnership_total += p.amount
        total_partnership_sum += partnership_total

    return jsonify({
        'year': year,
        'data': total_partnership_sum
    })

@app_look.route('/givings-yearly/<year>', methods=['GET'])
@jwt_required()
def get_total_givings_yearly(year):
    """Returns the total partnership for a given year"""

    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = storage.get_admin_users(admin_id)
    if not users:
        return jsonify({'message': 'No form data found'}), 401
    total_giving_sum = 0
    for user in users:
        try:
            date_obj = datetime.strptime(user.Date, '%Y-%m-%d')
        except ValueError:
            continue
        if date_obj.year != int(year):
            continue
        givings_total = 0
        for p in user.givings:
            try:
                date_obj = datetime.strptime(p.Date, '%Y-%m-%d')
            except ValueError:
                continue
            if date_obj.year != int(year):
                continue
            givings_total += p.amount
        total_giving_sum += givings_total
    return jsonify({
        'year': year,
        'data': total_giving_sum
    })

@app_look.route('/members', methods=['GET'])
@jwt_required()
def get_total_members():
    """Returns the total number of members"""
    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    try:
        users = storage.get_admin_users(admin_id)
        if not users:
            return jsonify({'message': 'No form data found'}), 401
        
        return jsonify({
            'data': len(users)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app_look.route('/partnership/<month>/<year>', methods=['GET'])
@jwt_required()
def get_total_partnership(month, year):
    """Returns the total partnership for a given month"""

    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = storage.get_admin_users(admin_id)
    if not users:
        return jsonify({'message': 'No form data found'}), 401
    total_partnership_sum = 0
    for user in users:
        partnership_total = 0
        for p in user.partnership:
            try:
                date_obj = datetime.strptime(p.Date, '%Y-%m-%d')
            except ValueError:
                continue
            if (month and date_obj.month != int(month)) or (year and date_obj.year != int(year)):
                continue
            partnership_total += p.amount
        total_partnership_sum += partnership_total
    return jsonify({
        'month': month,
        'year': year,
        'data': total_partnership_sum
    })
@app_look.route('/givings/<month>/<year>', methods=['GET'])
@jwt_required()
def get_total_givings(month, year):
    """Returns the total givings for a given month"""

    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    users = storage.get_admin_users(admin_id)
    if not users:
        return jsonify({'message': 'No form data found'}), 401
    total_giving_sum = 0
    for user in users:
        givings_total = 0
        for p in user.givings:
            try:
                date_obj = datetime.strptime(p.Date, '%Y-%m-%d')
            except ValueError:
                continue
            if (month and date_obj.month != int(month)) or (year and date_obj.year != int(year)):
                continue
            givings_total += p.amount
        total_giving_sum += givings_total
    return jsonify({
        'month': month,
        'year': year,
        'data': total_giving_sum
    })

