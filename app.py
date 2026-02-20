from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB connection configuration
# You can set these via environment variables or update directly
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'books2read')
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'books')

# Initialize MongoDB client
try:
    client = MongoClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    books_collection = db[COLLECTION_NAME]
    print(f"Connected to MongoDB: {DATABASE_NAME}")
except Exception as e:
    print(f"Warning: Could not connect to MongoDB: {e}")
    books_collection = None


@app.route('/')
def index():
    """Render the main page with search functionality"""
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Handle search requests and return books with hoursToRead less than or equal to input"""
    if books_collection is None:
        return jsonify({'error': 'Database connection not available'}), 500
    
    try:
        # Get search parameter
        hours_to_read = request.args.get('hoursToRead', type=float)
        
        if hours_to_read is None:
            return jsonify({'error': 'hoursToRead parameter is required'}), 400
        
        # Build query: only books with hoursToRead <= user input
        query = {'hoursToRead': {'$lte': hours_to_read}}
        
        # Execute search and only return title, pageCount, and image_url
        results = list(books_collection.find(
            query,
            {'title': 1, 'pageCount': 1, 'image_url': 1, '_id': 0}
        ).limit(50))
        
        return jsonify({
            'success': True,
            'count': len(results),
            'results': results
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        if books_collection is not None:
            # Test database connection
            books_collection.find_one()
            return jsonify({
                'status': 'healthy',
                'database': 'connected'
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'database': 'not connected'
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
