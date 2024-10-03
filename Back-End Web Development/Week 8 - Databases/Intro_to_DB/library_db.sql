-- Create a database named 'library_db'

CREATE DATABASE IF NOT EXISTS library_db;

-- Use the database

USE library_db;

-- Create a table named 'books'
CREATE TABLE IF NOT EXISTS books (
	id INT AUTO_INCREMENT PRIMARY KEY,
	title VARCHAR(255)NOT NULL,
	author VARCHAR(255)NOT NULL,
	isbn VARCHAR(255) NOT NULL
);

-- Insert some sample data into the 'books' table
-- Done
INSERT INTO books (title, author, isbn) VALUES ('1984', 'George Orwell', '9780451524935');
INSERT INTO books (title, author, isbn) VALUES ('To Kill a Mockingbird', 'Harper Lee', '9780060935467');


