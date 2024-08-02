from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from forms import BookForm
import sqlite3


app = Flask(__name__)
app.config['SECRET_KEY']='62e51ba14032cd63f3dbbf8840b4b266' 


DATABASE = 'books.db'

@app.route('/')
@app.route("/home")
def home():
    return render_template('home.html')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_book(title, author, published_date, isbn, pages, language, publisher):
 #insertion of a new book record into the database
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO books (title, author, published_date, isbn, pages, language, publisher)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, published_date, isbn, pages, language, publisher))
    conn.commit()
    conn.close()

@app.route('/api/books', methods=['POST'])
 #handles the creation of a book via a REST API
def api_create_book():
    data = request.get_json()
    
    if not data or not all(key in data for key in ('title', 'author', 'published_date', 'isbn', 'pages', 'language', 'publisher')):
        return jsonify({'error': 'Missing required fields'}), 400

    title = data['title']
    author = data['author']
    published_date = data['published_date']
    isbn = data['isbn']
    pages = data['pages']
    language = data['language']
    publisher = data['publisher']
    
    create_book(title, author, published_date, isbn, pages, language, publisher)#la fonction du creation
    
    response = {
        'title': title,
        'author': author,
        'published_date': published_date,
        'isbn': isbn,
        'pages': pages,
        'language': language,
        'publisher': publisher
    }
    return jsonify(response), 201 #The jsonify() function in Flask converts Python objects (like lists and dictionaries) into JSON format
                                  #Since sqlite3.Row objects are not serializable to JSON, converting them to dictionaries ensures that jsonify() can process them correctly


@app.route('/creation', methods=['GET', 'POST'])
#handles the creation of a book via an HTML form
def creation():
    try:
        form = BookForm()
        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            published_date = request.form['published_date']
            isbn = request.form['isbn']
            pages = request.form['pages']
            language = request.form['language']
            publisher = request.form['publisher']
            
            create_book(title, author, published_date, isbn, pages, language, publisher)
            flash('Book created successfully!', 'success')
            return redirect(url_for('list'))
        return render_template('creation.html',form=form)
    except Exception as e:
        print(f'error in book_detail function: {e}')
        return render_template('error_page.html',error_message=str(e))



@app.route('/api/books', methods=['GET'])
def api_get_books():
   # retrieves a list of books from a database and returns them in JSON format
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    books_list = [dict(book) for book in books] #convert each sqlite3.Row object into a dictionary
    return jsonify(books_list), 200 


@app.route('/list')
def list():
#ret rieves a list of books from a database and put them on a list
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('list.html', books=books)




@app.route('/delete_book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    #retrieve a book from the data base through the id
    conn = get_db_connection()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    
    return redirect(url_for('list'))
    return jsonify({}), 204 #An empty JSON object ({}) as the response body==>the DELETE method typically doesn't return any data in the response body


@app.route('/book/<int:book_id>', methods=['GET'])
def book_detail(book_id):
    try:
        conn = get_db_connection()
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        conn.close()
        
        if book is None:
            return jsonify({'error': 'Book not found'}), 404

        return render_template('book_detail.html', book=book)

    except Exception as e:
        print(f'error in book_detail function: {e}')
        return render_template('error_page.html')


#update
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def api_update_book(book_id):
    
        # Get the JSON data from the request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'author', 'published_date', 'isbn', 'pages', 'language', 'publisher']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Extract data from the JSON request
        title = data['title']
        author = data['author']
        published_date = data['published_date']
        isbn = data['isbn']
        pages = data['pages']
        language = data['language']
        publisher = data['publisher']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
        
        if book is None:
            conn.close()
            return jsonify({'error': 'Book not found'}), 404
        
        # Update 
        conn.execute(
            "UPDATE books SET title=?, author=?, published_date=?, isbn=?, pages=?, language=?, publisher=? WHERE id=?", 
            (title, author, published_date, isbn, pages, language, publisher, book_id)
        )
        conn.commit()
        conn.close()
        
        # Return the updated book details
        updated_book = {
            'id': book_id,
            'title': title,
            'author': author,
            'published_date': published_date,
            'isbn': isbn,
            'pages': pages,
            'language': language,
            'publisher': publisher
        }
        return jsonify(updated_book), 200


@app.route('/book/<int:book_id>/update', methods=['GET', 'POST'])
def update_book(book_id):
    form = BookForm()
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    
    if book is None:
        conn.close()
        return jsonify({'error': 'Book not found'}), 404

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        published_date = request.form.get('published_date')
        isbn = request.form.get('isbn')
        pages = request.form.get('pages')
        language = request.form.get('language')
        publisher = request.form.get('publisher')

        conn.execute(
            "UPDATE books SET title=?, author=?, published_date=?, isbn=?, pages=?, language=?, publisher=? WHERE id=?", 
            (title, author, published_date, isbn, pages, language, publisher, book_id)
        )
        conn.commit()
        conn.close()

        flash('Your Book has been updated!', 'success')
        return redirect(url_for('list'))

    conn.close()
    return render_template('update_book.html', book=book, form=form)

if __name__=='__main__':
    app.run(debug=True)