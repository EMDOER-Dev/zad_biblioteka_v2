from app import db

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f'<Author {self.name}>'

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='available')  # available or borrowed

    def __repr__(self):
        return f'<Book {self.title}>'