from flask import Flask, request, jsonify
from database.db import KingsRecordDatabase
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'secret_key')

if os.getenv('DEBUG') == 'False':
    app.config['DEBUG'] = False
else:
    app.config['DEBUG'] = True

# @app.teardown_appcontext
# def close_connection(exception=None):
#     KingsRecordDatabase.end_session()


@app.errorhandler(404)
def notFound(err):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)