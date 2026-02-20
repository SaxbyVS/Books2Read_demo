# Books2Read

A Flask web application for searching books based on reading time (hoursToRead).

## Features

- Search books by comparing `hoursToRead` field
- Multiple comparison operators (less than, equal to, greater than, etc.)
- Modern, responsive UI
- MongoDB integration

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure MongoDB connection:
   - Copy `.env.example` to `.env`
   - Update MongoDB connection string in `.env`
   - Or set environment variables directly

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## MongoDB Schema

Your books collection should have documents with at least a `hoursToRead` field:

```json
{
  "_id": ObjectId("..."),
  "title": "Book Title",
  "author": "Author Name",
  "hoursToRead": 5.5,
  "genre": "Fiction",
  "description": "Book description..."
}
```

## API Endpoints

- `GET /` - Main page with search interface
- `GET /search?hoursToRead=<number>&comparison=<type>` - Search books
  - `comparison` options: `less_than_or_equal`, `less_than`, `equal`, `greater_than_or_equal`, `greater_than`
- `GET /health` - Health check endpoint

## Example Usage

Search for books with 5 hours or less reading time:
```
http://localhost:5000/search?hoursToRead=5&comparison=less_than_or_equal
```
