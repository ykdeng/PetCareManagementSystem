from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import backref
from os import environ

app = Flask(__name__)
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    
    posts = db.relationship('Post', backref=backref('author', lazy=True), lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Post {self.title}>'

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL') or 'sqlite:///yourdefault.db'
app.config['SECRET_KEY'] = environ.get('SECRET_KEY') or 'yourdefaultsecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)