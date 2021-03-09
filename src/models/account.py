from db import db

class AccountModel(db.Model):
    
    __tablename__ = 'accounts'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20))
    name = db.Column(db.String(30))
    address = db.Column(db.String(100))
    state = db.Column(db.String(20))
    country = db.Column(db.String(20))
    email = db.Column(db.String(50))
    pan = db.Column(db.String(10))
    contact = db.Column(db.String(11))
    dob = db.Column(db.String(20))
    acc_type = db.Column(db.String(20))
    
    username = db.Column(db.Integer,db.ForeignKey("users.username"))
    user = db.relationship('UserModel')
    
    loans = db.relationship('LoanModel',lazy='dynamic')
    
    def __init__(self,username,name,address,state,country,email,pan,contact,dob,acc_type):
        self.username = username
        self.name=name 
        self.address=address 
        self.state=state 
        self.country=country 
        self.email=email 
        self.pan=pan 
        self.contact=contact    
        self.dob=dob
        self.acc_type=acc_type 
        
    def json(self):
        return {'username':self.username,"name":self.name,"address":self.address,"state":self.state,"country":self.country,"email":self.email,"pan":self.pan,"contact":self.contact,"dob":self.dob,"acc_type":self.acc_type,"userpass":self.user.password}   
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod    
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod    
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()