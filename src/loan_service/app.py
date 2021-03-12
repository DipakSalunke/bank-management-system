from flask import Flask
from flask_restful import Api
import logging


from db import db
from resources.loan import Loan

app = Flask(__name__)
logging.basicConfig(
    filename="./src/loan/record.log",
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
logging.info("log started")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Loan, "/loan")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5003, debug=True)
