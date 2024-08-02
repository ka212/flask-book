# Book Management System

A book management system built using Flask ==> a micro web framework for Python.

## Features

*   Create, read, update, and delete (CRUD) book records
*   REST API for creating, reading,  updating and deleting book records
*   User interface for creating, reading, updating and deleting  book records
*   Error handling for invalid requests and database errors

## API Endpoints
POST /api/books: Create a new book record
GET /api/books: Retrieve a list of all book records
GET /api/books/<int:book_id>: Retrieve a single book record by ID
PUT /api/books/<int:book_id>: Update a single book record by ID
DELETE /api/books/<int:book_id>: Delete a single book record by ID

