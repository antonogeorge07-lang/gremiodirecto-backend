from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gremiodirecto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    language = db.Column(db.String(10), default='es')

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return "Hello from GremioDirecto backend!"

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return {
        'users': [
            {
                'id': u.id,
                'type': u.type,
                'name': u.name,
                'email': u.email,
                'language': u.language
            }
            for u in users
        ]
    }

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        type=data['type'],
        name=data['name'],
        email=data['email'],
        language=data.get('language', 'es')
    )
    db.session.add(user)
    db.session.commit()
    return {
        'id': user.id,
        'type': user.type,
        'name': user.name,
        'email': user.email,
        'language': user.language
    }

@app.route('/workers', methods=['POST'])
def create_worker():
    data = request.get_json()
    user = User(
        type='worker',
        name=data['name'],
        email=data['email'],
        language=data.get('language', 'es')
    )
    db.session.add(user)
    db.session.commit()
    return {
        'id': user.id,
        'type': user.type,
        'name': user.name,
        'email': user.email,
        'language': user.language
    }

@app.route('/workers/available', methods=['GET'])
def get_available_workers():
    users = User.query.filter_by(type='worker').all()
    return {
        'workers': [
            {
                'id': u.id,
                'name': u.name,
                'email': u.email,
                'language': u.language
            }
            for u in users
        ]
    }

@app.route('/activity', methods=['POST'])
def create_activity():
    data = request.get_json()
    activity = Activity(
        description=data['description'],
        worker_id=data['worker_id']
    )
    db.session.add(activity)
    db.session.commit()
    return {
        'id': activity.id,
        'description': activity.description,
        'worker_id': activity.worker_id
    }

if __name__ == "__main__":
    app.run(debug=True, port=5000)