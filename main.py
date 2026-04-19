from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Production DB (Railway PostgreSQL)
db_url = os.environ.get('DATABASE_URL', 'sqlite:///gremiodirecto.db')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://')
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    language = db.Column(db.String(10), default='es')

# CREATE TABLES
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return jsonify({"message": "GremioDirecto Backend LIVE! 🚀"})

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": u.id, "type": u.type, "name": u.name,
        "email": u.email, "language": u.language
    } for u in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        type=data.get('type', 'worker'),
        name=data.get('name'),
        email=data.get('email'),
        language=data.get('language', 'es')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "id": user.id, "type": user.type, "name": user.name,
        "email": user.email, "language": user.language
    }), 201

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
