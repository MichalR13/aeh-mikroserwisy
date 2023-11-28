from flask_login import UserMixin, current_user
from flask import redirect, url_for, flash

class User():
    email = db.Column(db.String(50), unique=True, nullable=False)
    isAdmin = True
    #auth_token

    def __repr__(self):
        return '<User %r>' % (self.email)