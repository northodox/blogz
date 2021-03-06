from app import db
from hashutils import make_password_hash

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return '<Movie %r>' % self.title

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(60), unique = True)
    hashword = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref = 'owner')

    def __init__(self, username, hashword):
        self.username = username
        self.hashword = make_password_hash(hashword)

    def __repr__(self):
        return '<User %r>' %self.username