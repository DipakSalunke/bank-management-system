from db import db

class LoanModel(db.Model):
    
    __tablename__ = 'loans'
    id = db.Column(db.Integer,primary_key=True)
    loan_type = db.Column(db.String(20))
    loan_amt = db.Column(db.Float(150))
    date = db.Column(db.String(100))
    rate_of_int = db.Column(db.Float(3))
    duration = db.Column(db.Float(50))
    
    acc_id = db.Column(db.Integer)
    
    def __init__(self,date,acc_id,loan_type,loan_amt,rate_of_int,duration):
        self.acc_id = acc_id
        self.loan_type = loan_type
        self.loan_amt = loan_amt
        self.date = date
        self.rate_of_int  =rate_of_int
        self.duration = duration
        
    def json(self):
        return {"loan_id":self.id,'loan_type':self.loan_type,"loan_amt":self.loan_amt,"date":self.date,"rate_of_int":self.rate_of_int,"duration":self.duration}   
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod    
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod    
    def find_by_accid(cls,id):
        return cls.query.filter_by(acc_id=id)