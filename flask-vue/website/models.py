"""
mdoels.py

Register data relations!
"""

from website import db,login_manager,app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as serializer

stock_id_lists = {
    '000001.SZ':'./static/a.csv',
    '002371.SZ':'./static/b.csv',
    'AAPL':'/static/c.csv'
}

@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

def add_to_database(obj):
    db.session.add(obj)
    db.session.commit()

def delete_from_database(obj):
    db.session.delete(obj)
    db.session.commit()

class UserModel(db.Model,UserMixin):
    __tablename__= "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password =  db.Column(db.String(60),nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    
    def __repr__(self):
        return  "User {}  Email {}  Image {}".format(self.username,self.email,self.image)

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()
    
    def get_reset_token(self,expires_sec=1800):
        s = serializer(app.config['SECRET_KEY'],expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")
    
    @staticmethod
    def verify_reset_token(token):
        s = serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return UserModel.query.get(user_id)
    @staticmethod
    def find_by_stock_id(stock_id):
        if stock_id not in stock_id_lists:
            return False
        else:
            return True

def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()
