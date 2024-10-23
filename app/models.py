from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class StackElement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

    def __repr__(self) -> str:
        return f"StackElement(id={self.id!r}, value={self.value!r})"

