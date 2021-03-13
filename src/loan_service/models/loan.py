from db import db
from typing import List


class LoanModel(db.Model):

    __tablename__ = "loans"
    id = db.Column(db.Integer, primary_key=True)
    loan_type = db.Column(db.String(20), nullable=False)
    loan_amt = db.Column(db.Float(150), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    rate_of_int = db.Column(db.Float(3), nullable=False)
    duration = db.Column(db.Float(50), nullable=False)
    acc_id = db.Column(db.Integer, nullable=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> List["LoanModel"]:
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_accid(cls, id: int) -> List["LoanModel"]:
        return cls.query.filter_by(acc_id=id)
