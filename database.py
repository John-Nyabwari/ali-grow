import sqlite3
from datetime import datetime

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect('market_prices.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Create database tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create markets table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create crops table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT NOT NULL
        )
    ''')
    
    # Create prices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_id INTEGER,
            crop_id INTEGER,
            price REAL NOT NULL,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (market_id) REFERENCES markets(id),
            FOREIGN KEY (crop_id) REFERENCES crops(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def seed_sample_data():
    """Add sample markets, crops, and prices for testing."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM markets")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # Sample markets in Nairobi
    markets = [
        ('Wakulima Market', 'Nairobi'),
        ('City Market', 'Nairobi'),
        ('Muthurwa Market', 'Nairobi'),
        ('Kawangware Market', 'Nairobi'),
        ('Gikomba Market', 'Nairobi'),
        ('Maasai Market', 'Nairobi')
    ]
    
    cursor.executemany(
        "INSERT INTO markets (name, location) VALUES (?, ?)",
        markets
    )
    
    # Sample crops
    crops = [
        ('Tomatoes', 'Vegetables', 'kg'),
        ('Onions', 'Vegetables', 'kg'),
        ('Potatoes', 'Vegetables', 'kg'),
        ('Maize', 'Grains', 'kg'),
        ('Beans', 'Grains', 'kg'),
        ('Bananas', 'Fruits', 'bunch'),
        ('Mangoes', 'Fruits', 'kg'),
        ('Kale (Sukuma Wiki)', 'Vegetables', 'bunch')
    ]
    
    cursor.executemany(
        "INSERT INTO crops (name, category, unit) VALUES (?, ?, ?)",
        crops
    )
    
    # Sample prices (market_id, crop_id, price in KES)
    prices = [
        (1, 1, 80.00),   # Tomatoes at Wakulima
        (1, 2, 60.00),   # Onions at Wakulima
        (1, 3, 45.00),   # Potatoes at Wakulima
        (1, 4, 55.00),   # Maize at Wakulima
        (1, 5, 120.00),  # Beans at Wakulima
        (2, 1, 90.00),   # Tomatoes at City Market
        (2, 2, 70.00),   # Onions at City Market
        (3, 1, 75.00),   # Tomatoes at Muthurwa
        (3, 6, 150.00),  # Bananas at Muthurwa
        (4, 7, 100.00),  # Mangoes at Kawangware
        (5, 8, 30.00),
        (6, 4, 35.00)
    ]
    
    cursor.executemany(
        "INSERT INTO prices (market_id, crop_id, price) VALUES (?, ?, ?)",
        prices
    )
    
    conn.commit()
    conn.close()
    print("Sample data added successfully!")

def get_all_prices():
    """Get all prices with market and crop information."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            p.id,
            m.name as market_name,
            m.location,
            c.name as crop_name,
            c.category,
            c.unit,
            p.price,
            p.recorded_at
        FROM prices p
        JOIN markets m ON p.market_id = m.id
        JOIN crops c ON p.crop_id = c.id
        ORDER BY p.recorded_at DESC
    ''')
    
    prices = cursor.fetchall()
    conn.close()
    return prices

def add_market(name, location):
    """Add a new market."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO markets (name, location) VALUES (?, ?)",
        (name, location)
    )
    
    conn.commit()
    conn.close()
    
def get_prices_by_crop(crop_name):
    """Get prices for a specific crop across all markets."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT 
            m.name as market_name,
            m.location,
            c.name as crop_name,
            c.unit,
            p.price,
            p.recorded_at
        FROM prices p
        JOIN markets m ON p.market_id = m.id
        JOIN crops c ON p.crop_id = c.id
        WHERE c.name LIKE ?
        ORDER BY p.price ASC
    ''', (f'%{crop_name}%',))
    
    prices = cursor.fetchall()
    conn.close()
    return prices

def add_price(market_id, crop_id, price):
    """Add a new price entry."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO prices (market_id, crop_id, price) VALUES (?, ?, ?)",
        (market_id, crop_id, price)
    )
    
    conn.commit()
    conn.close()
    return True

def get_markets():
    """Get all markets."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM markets ORDER BY name")
    markets = cursor.fetchall()
    conn.close()
    return markets

def get_crops():
    """Get all crops."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crops ORDER BY category, name")
    crops = cursor.fetchall()
    conn.close()
    return crops

def add_price_comparison(market_id, crop_id, price):
    """Find cheapest and most expensive markets for a crop."""
    
    prices =get_prices_by_crop(crop_name)
    if not prices:
        return None, None
    
    cheapest = min(prices, key=lambda x: x['price'])
    most_expensive = max(prices, key=lambda x: x['price'])
    
    return{
        'crop': crop_name,
        'cheapest_market': cheapest['market_name'],
        'cheapest_price': cheapest['price'],
        'expensive_market': most_expensive['market_name'],
        'expensive_price': most_expensive['price'],
        'potential_savings': most_expensive['price'] - cheapest['price']
    }
    
    