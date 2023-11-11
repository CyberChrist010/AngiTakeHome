from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from urllib.parse import urlparse
import os
import string
import random

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uri_shorten.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.urandom(24)  # Use a secure random key
app.config['SECRET_KEY'] = os.urandom(24)  # Used by Flask-Limiter

# Extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Initialize Limiter without attaching the app on creation
limiter = Limiter(key_func=get_remote_address)
# Attach the app to the Limiter
limiter.init_app(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    shortcode = db.Column(db.String(32), unique=True, nullable=False)

# URL Validation Function
def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return all([parsed.scheme, parsed.netloc, parsed.scheme in ["http", "https"]])
    except:
        return False

# Create database tables
with app.app_context():
    db.create_all()

# Helper functions (Generate a shortcode avoiding collisions)
def generate_shortcode(length=6):
    shortcode = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    if ShortURL.query.filter_by(shortcode=shortcode).first() is not None:
        return generate_shortcode(length)  # Recursively generate a new code
    return shortcode

# Routes
@app.route('/')
def home():
    return jsonify({'message': 'Welcome to the API'})

@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already taken"}), 409

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Bad username or password"}), 401

# Shortens URL ensuring only valid URLs are provided
@app.route('/shorten', methods=['POST'])
@jwt_required()
def shorten():
    original_url = request.json.get('url')
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL provided. Please use a properly formatted URL with http or https scheme.'}), 400

    shortcode = generate_shortcode()
    short_url = ShortURL(original_url=original_url, shortcode=shortcode)
    db.session.add(short_url)
    db.session.commit()

    return jsonify(shortcode=shortcode), 201

@app.route('/<shortcode>')
def redirect_to_url(shortcode):
    short_url = ShortURL.query.filter_by(shortcode=shortcode).first_or_404()
    return jsonify(original_url=short_url.original_url)

# Run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', ssl_context=('/app/cert.pem', '/app/newkey.pem'))

