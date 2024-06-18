from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models import Book, Author

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/library')
    def library():
        books = Book.query.all()
        return render_template('library.html', books=books)

    @app.route('/author/<int:author_id>')
    def author_books(author_id):
        author = Author.query.get_or_404(author_id)
        books = Book.query.filter_by(author_id=author.id).all()
        return render_template('author_books.html', author=author, books=books)

    @app.route('/add_author', methods=['GET', 'POST'])
    def add_author():
        if request.method == 'POST':
            name = request.form['name']
            if name:
                new_author = Author(name=name)
                db.session.add(new_author)
                db.session.commit()
                flash('Autor został dodany pomyślnie!')
                return redirect(url_for('library'))
            else:
                flash('Nazwa autora jest wymagana!')
        return render_template('add_author.html')

    @app.route('/add_book', methods=['GET', 'POST'])
    def add_book():
        authors = Author.query.all()
        if request.method == 'POST':
            title = request.form['title']
            author_id = request.form['author_id']
            year = request.form['year']
            status = request.form['status']

            if title and author_id and year and status:
                new_book = Book(title=title, author_id=author_id, year=int(year), status=status)
                db.session.add(new_book)
                db.session.commit()
                flash('Książka została dodana pomyślnie!')
                return redirect(url_for('library'))
            else:
                flash('Wszystkie pola są wymagane!')

        return render_template('add_book.html', authors=authors)

    @app.route('/delete_book/<int:book_id>', methods=['POST'])
    def delete_book(book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        flash('Książka została usunięta!')
        return redirect(url_for('edit'))

    @app.route('/delete_author/<int:author_id>', methods=['POST'])
    def delete_author(author_id):
        author = Author.query.get_or_404(author_id)
        db.session.delete(author)
        db.session.commit()
        flash('Autor został usunięty!')
        return redirect(url_for('edit'))

    @app.route('/edit')
    def edit():
        books = Book.query.all()
        authors = Author.query.all()
        return render_template('edit.html', books=books, authors=authors)

    @app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
    def edit_book(book_id):
        book = Book.query.get_or_404(book_id)
        authors = Author.query.all()

        if request.method == 'POST':
            book.title = request.form['title']
            book.author_id = request.form['author_id']
            book.year = request.form['year']
            book.status = request.form['status']

            db.session.commit()
            flash('Książka została zaktualizowana!')
            return redirect(url_for('edit'))

        return render_template('edit_book.html', book=book, authors=authors)

    @app.route('/edit_author/<int:author_id>', methods=['GET', 'POST'])
    def edit_author(author_id):
        author = Author.query.get_or_404(author_id)

        if request.method == 'POST':
            author.name = request.form['name']

            db.session.commit()
            flash('Autor został zaktualizowany!')
            return redirect(url_for('edit'))

        return render_template('edit_author.html', author=author)

    return app
