from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------------- USER ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20), default="user")  # user / admin
    #--PROFILE IMAGE---
    photo = db.Column(db.String(200), default="Krish.jpg")


# -------- ELECTRICIAN --------
class Electrician(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    time = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='electrician', lazy=True)


# -------- JOB --------
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    deadline = db.Column(db.String(50))

    electrician_id = db.Column(db.Integer, db.ForeignKey('electrician.id'))
    electrician = db.relationship('Electrician')

    time = db.Column(db.DateTime, default=datetime.utcnow)


# -------- TASK --------
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    status = db.Column(db.String(50))

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    electrician_id = db.Column(db.Integer, db.ForeignKey('electrician.id'))

    job = db.relationship('Job')

    time = db.Column(db.DateTime, default=datetime.utcnow)


# -------- MATERIAL --------
class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)

    time = db.Column(db.DateTime, default=datetime.utcnow)