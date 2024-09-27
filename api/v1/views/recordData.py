from flask_jwt_extended import get_jwt_identity, jwt_required
from flask import jsonify, request, redirect, abort
from api.v1.views import app_look
from database.db import KingsRecordDatabase
from datetime import datetime

storage = KingsRecordDatabase()

@app_look.route('/form-data', methods=['PUT'])
@jwt_required()
def handle_form_data():
    """Handles the form data"""
    admin_id = get_jwt_identity()
    if not admin_id:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    kwargs = {
        'title': data.get('title'),
        'firstName': data.get('firstName'),
        'lastName': data.get('lastName'),
        'Date': data.get('Date'),
        'email': data.get('email'),
        'phoneNumber': data.get('phoneNumber')
    }
    partnerships = data.get('partnerships', [])
    givings = data.get('givings', [])

    if not kwargs['title'] or not kwargs['firstName'] or not kwargs['lastName'] or not kwargs['Date'] \
    or not kwargs['email'] or not kwargs['phoneNumber']:
        return jsonify({'error': 'All fields are required'}), 400
    if not partnerships or not givings:
        return jsonify({'error': 'At least one partnership and one giving must be provided'}), 400
    print( kwargs['email'], kwargs['phoneNumber'], partnerships, givings)

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
                    chk_user.add_partnership(type_details, amount, createdAt=datetime.now())

        if givings:
            for give in givings:
                if 'type' not in give or 'amount' not in give:
                    return jsonify({'error': 'Invalid giving format'}), 400
                give_type, gift_amount = give['type'], give['amount']
                existing_giving = next((g for g in chk_user.givings if g.type == give_type), None)
                if existing_giving:
                    existing_giving.amount += gift_amount
                    existing_giving.updatedAt = datetime.now()
                else:
                    chk_user.add_giving(give_type, gift_amount, createdAt=datetime.now())
        chk_user.save()
        return jsonify({'message': 'User data updated successfully'}), 200
    else:
        new_user = storage.reg_user(**kwargs)
        if new_user is None:
            return jsonify({'error': 'User registration failed'}), 500
        if partnerships:
            for partner in partnerships:
                type_details, amount = partner['type'], partner['amount']
                new_user.add_partnership(type_details, amount, createdAt=datetime.now())
        if givings:
            for give in givings:
                give_type, give_amount = give['type'], give['amount']
                new_user.add_giving(give_type, give_amount, createdAt=datetime.now())
        new_user.save()
        return jsonify({'message': 'User data created successfully'}), 201
    

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
        try:
            date_obj = datetime.strptime(user.Date, '%Y-%m-%d')
        except ValueError:
            continue
        if (month and date_obj.month != int(month)) or (year and date_obj.year != int(year)):
            continue
        partnership_total = 0
        givings_total = 0
        for p in user.partnership:
            partnership_total += p.amount
        
        for g in user.givings:
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
            'partnerships': [{'type': p.type, 'amount': p.amount} for p in user.partnership],
            'givings': [{'type': g.type, 'amount': g.amount} for g in user.givings],
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
        try:
            date_obj = datetime.strptime(user.Date, '%Y-%m-%d')
        except ValueError:
            continue
        if date_obj.year != int(year):
            continue
        partnership_total = 0
        for p in user.partnership:
            partnership_total += p.amount
        total_partnership_sum += partnership_total

    return jsonify({
        'year': year,
        'total_partnership_sum': total_partnership_sum
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
            givings_total += p.amount
        total_giving_sum += givings_total
    return jsonify({
        'year': year,
        'total_partnership_sum': total_giving_sum
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
            'total_members': len(users)
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
        try:
            date_obj = datetime.strptime(user.Date, '%Y-%m-%d')
        except ValueError:
            continue
        if (month and date_obj.month != int(month)) or (year and date_obj.year != int(year)):
            continue
        partnership_total = 0
        for p in user.partnership:
            partnership_total += p.amount
        total_partnership_sum += partnership_total
    return jsonify({
        'month': month,
        'year': year,
        'total_partnership_sum': total_partnership_sum
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
        try:
            date_obj = datetime.strptime(user.Date, '%Y-%m-%d')
        except ValueError:
            continue
        if (month and date_obj.month != int(month)) or (year and date_obj.year != int(year)):
            continue
        givings_total = 0
        for p in user.givings:
            givings_total += p.amount
        total_giving_sum += givings_total
    return jsonify({
        'month': month,
        'year': year,
        'total_giving_sum': total_giving_sum
    })

