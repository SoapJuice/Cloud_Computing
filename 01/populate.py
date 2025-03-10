import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# Create Books Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL
)
""")

# Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

# Create Loans Table (Tracks borrowed books)
cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    loan_date TEXT NOT NULL,
    return_date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(book_id) REFERENCES books(id)
)
""")

# Sample book data
books = [
    ("The Catcher in the Rye", "J.D. Salinger", "Fiction"),
    ("To Kill a Mockingbird", "Harper Lee", "Classic"),
    ("1984", "George Orwell", "Dystopian"),
    ("The Great Gatsby", "F. Scott Fitzgerald", "Classic"),
    ("Moby-Dick", "Herman Melville", "Adventure"),
]

# Sample users
users = [
    ("Alice Johnson", "alice@example.com"),
    ("Bob Smith", "bob@example.com"),
]

# Sample loan data
loans = [
    (1, 1, "2024-03-09", "2024-03-16"),  # Alice borrowed "The Catcher in the Rye"
    (2, 3, "2024-03-08", None),  # Bob borrowed "1984" (not yet returned)
]

# Insert data into tables
cursor.executemany("INSERT INTO books (name, author, genre) VALUES (?, ?, ?)", books)
cursor.executemany("INSERT INTO users (name, email) VALUES (?, ?)", users)
cursor.executemany("INSERT INTO loans (user_id, book_id, loan_date, return_date) VALUES (?, ?, ?, ?)", loans)

# Commit changes and close connection
conn.commit()
conn.close()

print("Library database setup complete!")
