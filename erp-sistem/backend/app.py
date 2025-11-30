from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'erpdb'),
    'user': os.getenv('POSTGRES_USER', 'erpuser'),
    'password': os.getenv('POSTGRES_PASSWORD', 'erppassword'),
    'port': os.getenv('DB_PORT', '5432')
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    """Initialize database tables"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def home():
    return jsonify({
        'message': 'ERP System API',
        'version': '1.0',
        'endpoints': {
            'GET /api/products': 'Get all products',
            'POST /api/products': 'Create a product',
            'GET /api/health': 'Health check'
        }
    })

@app.route('/api/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, name, price, quantity, created_at FROM products ORDER BY id DESC')
        products = []
        for row in cur.fetchall():
            products.append({
                'id': row[0],
                'name': row[1],
                'price': float(row[2]),
                'quantity': row[3],
                'created_at': row[4].isoformat() if row[4] else None
            })
        cur.close()
        conn.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        quantity = data.get('quantity')

        if not all([name, price is not None, quantity is not None]):
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s) RETURNING id',
            (name, price, quantity)
        )
        product_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({
            'id': product_id,
            'name': name,
            'price': price,
            'quantity': quantity,
            'message': 'Product created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
