# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Create Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

# Define Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

# Create database tables
def add_context():
    with app.app_context():
        db.create_all()

# Define routes

# Route to display list of books
@app.route('/books')
def books():
    book_list = Book.query.all()
    return render_template('books.html', books=book_list)

# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pub_year = request.form['pub_year']

        new_book = Book(title=title, author=author, publication_year=pub_year)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('books'))

    return render_template('add_book.html')

# Run the app
if __name__ == '__main__':
    # Add context before running the app to create tables
    add_context()
    app.run(debug=True)
