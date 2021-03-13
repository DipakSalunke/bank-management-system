from db import db
from typing import Dict, List, Union

# AccountJSON = Dict[str, Union[float]]


class AccountModel(db.Model):

    __tablename__ = "accounts"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    pan = db.Column(db.String(10), nullable=False)
    contact = db.Column(db.String(11), nullable=False)
    dob = db.Column(db.String(20), nullable=False)
    acc_type = db.Column(db.String(20), nullable=False)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "AccountModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, id: int) -> "AccountModel":
        return cls.query.filter_by(id=id).first()
