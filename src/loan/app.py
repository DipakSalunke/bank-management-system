from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
import logging


from db import db
from resources.loan import Loan

app = Flask(__name__)
logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
log = logging.getLogger()
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True 
app.secret_key = 'dipak'
api = Api(app)
@app.before_first_request
def create_tables():
    db.create_all()
    
api.add_resource(Loan,"/loan")

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5003,debug=True)