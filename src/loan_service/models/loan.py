from db import db
from typing import Dict, List, Union

LoanJSON = Dict[str, Union[str, int, float]]


class LoanModel(db.Model):

    __tablename__ = "loans"
    id = db.Column(db.Integer, primary_key=True)
    loan_type = db.Column(db.String(20))
    loan_amt = db.Column(db.Float(150))
    date = db.Column(db.String(100))
    rate_of_int = db.Column(db.Float(3))
    duration = db.Column(db.Float(50))

    acc_id = db.Column(db.Integer)

    def __init__(
        self,
        date: str,
        acc_id: int,
        loan_type: str,
        loan_amt: float,
        rate_of_int: float,
        duration: float,
    ):
        self.acc_id = acc_id
        self.loan_type = loan_type
        self.loan_amt = loan_amt
        self.date = date
        self.rate_of_int = rate_of_int
        self.duration = duration

    def json(self) -> LoanJSON:
        return {
            "loan_id": self.id,
            "loan_type": self.loan_type,
            "loan_amt": self.loan_amt,
            "date": self.date,
            "rate_of_int": self.rate_of_int,
            "duration": self.duration,
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> List["LoanModel"]:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_accid(cls, id: int) -> List["LoanModel"]:
        return cls.query.filter_by(acc_id=id)
