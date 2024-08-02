CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published_date DATE,
    isbn TEXT UNIQUE NOT NULL,
    pages INTEGER,
    language TEXT,
    publisher TEXT
);

