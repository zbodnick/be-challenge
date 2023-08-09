from app import db

class Lighter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_uri = db.Column(db.String(300), nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)

    def __repr__(self):
        return f"Lighter(id={self.id}, name='{self.name}', description={self.description})"
    
class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_uri = db.Column(db.String(300), nullable=False)
    
    # Establish many-to-one relationship
    lighters = db.relationship('Lighter', backref='manufacturer', lazy=True)

    #  method to return useful dev info on query obj
    def __repr__(self):
        return f"Manufacturer(id={self.id}, name='{self.name}')"