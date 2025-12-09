from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Swagger configuration
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"
}

swagger_template = {
    "info": {
        "title": "ERP System API",
        "description": "API documentation for ERP System - Product Management",
        "version": "1.0.0"
    },
    "schemes": ["http", "https"]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

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
    """
    API Information Endpoint
    ---
    tags:
      - General
    responses:
      200:
        description: API information and available endpoints
        schema:
          type: object
          properties:
            message:
              type: string
              example: ERP System API
            version:
              type: string
              example: "1.0"
            endpoints:
              type: object
    """
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
    """
    Health Check Endpoint
    ---
    tags:
      - General
    responses:
      200:
        description: Service is healthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            database:
              type: string
              example: connected
      500:
        description: Service is unhealthy
        schema:
          type: object
          properties:
            status:
              type: string
              example: unhealthy
            error:
              type: string
    """
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """
    Get All Products
    ---
    tags:
      - Products
    responses:
      200:
        description: List of all products
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Laptop"
              price:
                type: number
                format: float
                example: 999.99
              quantity:
                type: integer
                example: 10
              created_at:
                type: string
                format: date-time
                example: "2024-12-09T10:00:00"
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    Create a New Product
    ---
    tags:
      - Products
    parameters:
      - in: body
        name: body
        description: Product object that needs to be added
        required: true
        schema:
          type: object
          required:
            - name
            - price
            - quantity
          properties:
            name:
              type: string
              example: "Laptop"
              description: Product name
            price:
              type: number
              format: float
              example: 999.99
              description: Product price
            quantity:
              type: integer
              example: 10
              description: Product quantity in stock
    responses:
      201:
        description: Product created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            name:
              type: string
              example: "Laptop"
            price:
              type: number
              example: 999.99
            quantity:
              type: integer
              example: 10
            message:
              type: string
              example: "Product created successfully"
      400:
        description: Missing required fields
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Missing required fields"
      500:
        description: Internal server error
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
