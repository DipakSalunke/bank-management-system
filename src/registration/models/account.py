from db import db

class AccountModel:
    
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
        return {'username':self.username,"name":self.name,"address":self.address,"state":self.state,"country":self.country,"email":self.email,"pan":self.pan,"contact":self.contact,"dob":self.dob,"acc_type":self.acc_type}   