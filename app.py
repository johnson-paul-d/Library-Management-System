from flask import Flask, request, render_template, jsonify
from db import get_db_connection
from datetime import date

app = Flask(__name__)

# Routes for Pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books_page():
    return render_template('books.html')

@app.route('/members')
def members_page():
    return render_template('members.html')

@app.route('/transactions')
def transactions_page():
    return render_template('transactions.html')

# API Routes
@app.route('/api/books', methods=['GET'])
def get_books():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Books")
        return jsonify(cursor.fetchall())

@app.route('/api/books/add', methods=['POST'])
def add_book():
    data = request.json
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Books (title, author, genre, stock, rent_fee) VALUES (%s, %s, %s, %s, %s)",
                        (data['title'], data['author'], data['genre'], data['stock'], data['rent_fee']))
            conn.commit()
        return jsonify({"message": "Book added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/books/delete/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Books WHERE book_id = %s", (book_id,))
        conn.commit()
    return jsonify({"message": "Book deleted successfully"})

from datetime import datetime

@app.route('/api/issue', methods=['POST'])
def issue_book():
    data = request.json
    member_id = data['member_id']
    book_id = data['book_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if member has outstanding debt over ₹500
    cursor.execute("SELECT outstanding_debt FROM Members WHERE member_id = %s", (member_id,))
    member = cursor.fetchone()
    if not member or member[0] > 500:
        return jsonify({"error": "Member's outstanding debt exceeds ₹500"}), 400

    # Check if the book is in stock
    cursor.execute("SELECT stock FROM Books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    if not book or book[0] <= 0:
        return jsonify({"error": "Book is out of stock"}), 400

    # Insert the transaction with the current date and time
    cursor.execute(
        "INSERT INTO Transactions (book_id, member_id, issue_date) VALUES (%s, %s, NOW())",
        (book_id, member_id)
    )

    # Reduce stock
    cursor.execute("UPDATE Books SET stock = stock - 1 WHERE book_id = %s", (book_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Book issued successfully!", "issue_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}), 201


@app.route('/api/return', methods=['POST'])
def return_book():
    data = request.json
    member_id = data['member_id']
    book_id = data['book_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Find the transaction where the book was issued but not yet returned
    cursor.execute("""
        SELECT transaction_id, issue_date FROM Transactions 
        WHERE book_id = %s AND member_id = %s AND return_date IS NULL
        ORDER BY issue_date DESC LIMIT 1
    """, (book_id, member_id))
    
    transaction = cursor.fetchone()
    if not transaction:
        conn.close()
        return jsonify({"error": "No active transaction found for this book and member"}), 400

    transaction_id, issue_date = transaction

    # Calculate rent fee (₹10 per day)
    rent_fee = max(0, (datetime.now().date() - issue_date).days * 10)

    # Update the transaction record with return date and rent fee
    cursor.execute("""
        UPDATE Transactions SET return_date = NOW(), rent_fee = %s 
        WHERE transaction_id = %s
    """, (rent_fee, transaction_id))

    # Increase book stock
    cursor.execute("UPDATE Books SET stock = stock + 1 WHERE book_id = %s", (book_id,))

    conn.commit()
    conn.close()

    return jsonify({"message": "Book returned successfully!", "return_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "rent_fee": rent_fee}), 200

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.transaction_id, b.title, m.name AS member_name, t.issue_date, t.return_date, t.rent_fee
            FROM Transactions t
            LEFT JOIN Books b ON t.book_id = b.book_id
            LEFT JOIN Members m ON t.member_id = m.member_id
            ORDER BY t.issue_date DESC
        """)
        return jsonify(cursor.fetchall())

@app.route('/api/members', methods=['GET'])
def get_members():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Members")
        return jsonify(cursor.fetchall())

@app.route('/api/members/add', methods=['POST'])
def add_member():
    data = request.json
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Members (name, email, phone) VALUES (%s, %s, %s)", 
                    (data['name'], data['email'], data['phone']))
        conn.commit()
    return jsonify({"message": "Member added successfully"})

@app.route('/api/members/delete/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Members WHERE member_id = %s", (member_id,))
        conn.commit()
    return jsonify({"message": "Member deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
