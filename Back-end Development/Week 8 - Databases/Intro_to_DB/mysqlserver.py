import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error


def connect_to_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass ("Enter password: "),
        database="library_db"
    )
    return mydb

mydb = connect_to_db()
mycursor = mydb.cursor()

#  Insert new records into the book table
def add_book(title, author, isbn):
    sql = "INSERT INTO books (title, author, ISBN) VALUES (%s, %s, %s)"
    val = (title, author, isbn)
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"Book '{title}' added successfully.")

# Function that allows users to search for books by title
def search_books(title):
    sql = "SELECT * FROM books WHERE title LIKE %s"
    val = ("%"+title+"%",)
    mycursor.execute(sql, val)
    results = mycursor.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("No books found with that title.")

# Listing all books
def list_all_books():
    mycursor.execute("SELECT * FROM books")
    results = mycursor.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print("No books found in the library.")

# Delete a book by its ID
def delete_book(book_id):
    sql = "DELETE FROM books WHERE id = %s"
    val = (book_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(f"Book with ID {book_id} deleted successfully.")

# Example usage
add_book("The Great Gatsby", "F. Scott Fitzgerald", "1234567890")
add_book("1984", "George Orwell", "0987654321")

print("Listing all books:")
list_all_books()

print("\nSearching for '1984':")
search_books("1984")

print("\nDeleting book with ID 1:")
delete_book(1)

print("\nListing all books again:")
list_all_books()

mycursor.close()
mydb.close()
