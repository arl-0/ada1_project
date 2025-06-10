from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    clearance = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(10), nullable=False)

class ADAEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_number = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    redacted_text = db.Column(db.Text, nullable=False)
    clearance_level = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class ChangeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('ada_entry.id'))
    edited_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(200))

    asset = db.relationship('ADAEntry', backref='changelog')
    editor = db.relationship('User')


# this is a test to make sure the github repo is working
# Add any additional models here as needed