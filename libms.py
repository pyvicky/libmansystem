import sqlite3

def connect_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books (
                 book_id TEXT PRIMARY KEY,
                 title TEXT,
                 author TEXT,
                 issued INTEGER
              )''')
    conn.commit()
    return conn

def create_book(conn, book_id, title, author):
    c = conn.cursor()
    c.execute("INSERT INTO books VALUES (?, ?, ?, ?)", (book_id, title, author, 0))
    conn.commit()
    print("Book added successfully!.")

def issue_book(conn, book_id):
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
    book = c.fetchone()
    if book:
        if not book[3]:
            c.execute("UPDATE books SET issued=? WHERE book_id=?", (1, book_id,))
            conn.commit()
            print("Book issued successfully.")
        else:
            print("Book already issued.")
    else:
        print("Book ID not found.")

def return_book(conn, book_id):
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
    book = c.fetchone()
    if book:
        if book[3]:
            c.execute("UPDATE books SET issued=? WHERE book_id=?", (0, book_id))
            conn.commit()
            print("Book returned successfully")
        else:
            print("Book is not issued")
    else:
        print("Book ID not found")

def delete_book(conn, book_id):
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    conn.commit()
    print("Book deleted successfully.")

def display_books(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    if books:
        print("Books in Library: ")
        for book in books:
            print(f"Book ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Issued: {'Yes' if book[3] else 'No'}")
    else:
        print("No books found in the library")

def main():
    conn = connect_database()
    while True:
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. Delete Book")
        print("5. Display books")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            book_id = input("Enter Book ID: ")
            title = input("Enter Title: ")
            author = input("Enter Author: ")
            create_book(conn, book_id, title, author)
        elif choice == '2':
            book_id = input("Enter Book ID: ")
            issue_book(conn, book_id)
        elif choice == '3':
            book_id = input("Enter Book ID: ")
            return_book(conn, book_id)
        elif choice == '4':
            book_id = input("Enter Book ID: ")
            delete_book(conn, book_id)
        elif choice == '5':
            display_books(conn)
        elif choice == '6':
            print("Exiting")
            conn.close()
            break
        else:
            print("Invalid choice, please enter a valid number")

if __name__ == "__main__":
    main()
