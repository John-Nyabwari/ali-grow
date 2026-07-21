# Project 1: Agricultural Market Price Transparency 🌾

## Problem Statement
Farmers in Kenya receive 30-40% lower prices for their crops because they lack real-time market information. Middlemen exploit this information asymmetry, buying at low prices and selling at high margins. This project creates a web app that shows real-time crop prices across different markets.

## Who Benefits
- **Smallholder farmers** - Get fair prices by knowing market rates
- **Cooperatives** - Can negotiate better deals with bulk information
- **Consumers** - Can find the best prices for food
- **Economy** - Reduces food waste and improves food security

## Learning Objectives
By completing this project, you will learn:
1. **Python** - Backend API development with Flask
2. **SQL** - Database design and queries
3. **HTML/CSS** - Web interface design
4. **REST APIs** - How frontend and backend communicate
5. **CRUD operations** - Create, Read, Update, Delete data

## Tech Stack
- **Backend:** Python + Flask
- **Database:** SQLite (simple, no setup needed)
- **Frontend:** HTML + CSS + JavaScript
- **Deployment:** Railway (free tier)

---

## Phase 1: Understanding the Problem

### Real-World Context
In Kenya, a farmer in Nakuru might grow tomatoes but not know that prices in Nairobi's Wakulima Market are 50% higher than at the local market. Without transportation info or market data, they sell to middlemen at low prices.

### Existing Solutions
- **Twiga Foods** - B2B platform for fresh produce (limited to large buyers)
- **iProcure** - Agricultural input supply chain (doesn't cover price data)
- **Government markets** - Physical notice boards (outdated, localized)

### Our Gap
No simple, accessible platform showing real-time prices across multiple markets for different crops.

---

## Phase 2: Planning the Solution

### MVP Features
1. Display current prices for different crops
2. Show prices by market location
3. Allow adding new price entries
4. Filter by crop type or market
5. Responsive design for mobile use

### Database Schema
```
TABLE markets (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

TABLE crops (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    unit TEXT NOT NULL
)

TABLE prices (
    id INTEGER PRIMARY KEY,
    market_id INTEGER,
    crop_id INTEGER,
    price REAL NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (market_id) REFERENCES markets(id),
    FOREIGN KEY (crop_id) REFERENCES crops(id)
)
```

### Architecture
```
[Browser] --> [HTML/CSS/JS] --> [Flask API] --> [SQLite Database]
    |              |                  |                |
    |              |                  |                |
[User sees]  [Form inputs]    [REST endpoints]  [Data storage]
```

---

## Phase 3: Hands-On Coding

### Step 1: Project Setup

Create a folder structure:
```
01-Agricultural-Prices/
├── app.py              # Main Python application
├── database.py         # Database setup and queries
├── templates/
│   └── index.html      # Main web page
├── static/
│   └── style.css       # Styling
└── requirements.txt    # Python dependencies
```

### Step 2: Database Setup (database.py)

```python
# database.py - This file handles all database operations
# LEARNING: SQLite is a lightweight database that stores data in a single file
# No need to install a separate database server!

import sqlite3
from datetime import datetime

# LEARNING: This function creates a connection to our database
# If the database file doesn't exist, SQLite creates it automatically
def get_connection():
    """Create and return a database connection."""
    # LEARNING: 'with' statement ensures the connection is properly closed
    # even if an error occurs
    conn = sqlite3.connect('market_prices.db')
    # LEARNING: Row factory makes it easier to access data by column name
    # Instead of result[0], you can use result['name']
    conn.row_factory = sqlite3.Row
    return conn

# LEARNING: This function sets up our database tables
# Called once when the application starts
def init_database():
    """Create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # LEARNING: SQL CREATE TABLE statement defines the structure of our data
    # PRIMARY KEY = unique identifier for each row
    # NOT NULL = this field cannot be empty
    # FOREIGN KEY = links to another table's primary key
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS markets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            unit TEXT NOT NULL
        )
    ''')
    
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
    
    # LEARNING: commit() saves the changes to the database
    # Without this, changes would be lost when connection closes
    conn.commit()
    conn.close()

# LEARNING: This function adds sample data for testing
# In real apps, data would come from users or APIs
def seed_sample_data():
    """Add sample markets, crops, and prices for testing."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM markets")
    if cursor.fetchone()[0] > 0:
        conn.close()
        return
    
    # LEARNING: INSERT INTO adds new rows to a table
    # The ? placeholders prevent SQL injection attacks
    # This is a critical security practice!
    
    # Sample markets in Kenya
    markets = [
        ('Wakulima Market', 'Nairobi'),
        ('City Market', 'Nairobi'),
        ('Muthurwa Market', 'Nairobi'),
        ('Kawangware Market', 'Nairobi'),
        ('Gikomba Market', 'Nairobi')
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
    
    # Sample prices (realistic Kenyan market prices)
    # Format: (market_id, crop_id, price in KES)
    prices = [
        (1, 1, 80.00),   # Tomatoes at Wakulima
        (1, 2, 60.00),   # Onions at Wakulima
        (1, 3, 45.00),   # Potatoes at Wakulima
        (1, 4, 55.00),   # Maize at Wakulima
        (1, 5, 120.00),  # Beans at Wakulima
        (2, 1, 90.00),   # Tomatoes at City Market (higher prices)
        (2, 2, 70.00),   # Onions at City Market
        (3, 1, 75.00),   # Tomatoes at Muthurwa
        (3, 6, 150.00),  # Bananas at Muthurwa
        (4, 7, 100.00),  # Mangoes at Kawangware
        (5, 8, 30.00)    # Kale at Gikomba
    ]
    
    cursor.executemany(
        "INSERT INTO prices (market_id, crop_id, price) VALUES (?, ?, ?)",
        prices
    )
    
    conn.commit()
    conn.close()
    print("Sample data added successfully!")

# LEARNING: Database query functions
# These functions retrieve data from our database

def get_all_prices():
    """Get all prices with market and crop information."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # LEARNING: JOIN combines data from multiple tables
    # We want to show market name, crop name, and price together
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
    
    # LEARNING: fetchall() returns all matching rows as a list
    prices = cursor.fetchall()
    conn.close()
    return prices

def get_prices_by_crop(crop_name):
    """Get prices for a specific crop across all markets."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # LEARNING: WHERE clause filters results
    # The LIKE operator allows partial matching
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
    
    # LEARNING: This inserts a new price record
    # The timestamp is automatically added by SQLite
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
```

### Step 3: Flask Application (app.py)

```python
# app.py - Main application file
# LEARNING: Flask is a lightweight Python web framework
# It handles HTTP requests and routes them to the right functions

from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import init_database, seed_sample_data, get_all_prices, get_prices_by_crop, add_price, get_markets, get_crops

# LEARNING: Create a Flask application instance
# The name '__name__' tells Flask where to look for templates and static files
app = Flask(__name__)

# LEARNING: This decorator tells Flask to run this function when someone visits '/'
# The function name can be anything, but the route '/' is what matters
@app.route('/')
def index():
    """Home page - display all prices."""
    # LEARNING: fetch all prices from database
    prices = get_all_prices()
    # LEARNING: render_template loads an HTML file from the templates folder
    # We pass the prices data so the template can display it
    return render_template('index.html', prices=prices)

@app.route('/prices')
def prices_page():
    """Prices page with filtering."""
    # LEARNING: request.args.get() gets URL parameters
    # Example: /prices?crop=tomatoes
    crop_filter = request.args.get('crop', '')
    
    if crop_filter:
        prices = get_prices_by_crop(crop_filter)
    else:
        prices = get_all_prices()
    
    return render_template('index.html', prices=prices, filter=crop_filter)

@app.route('/add-price', methods=['GET', 'POST'])
def add_price_page():
    """Page to add new price entries."""
    # LEARNING: request.method tells us if this is a GET or POST request
    # GET = user is viewing the form
    # POST = user submitted the form
    
    if request.method == 'POST':
        # LEARNING: Get form data from the request
        market_id = request.form.get('market_id')
        crop_id = request.form.get('crop_id')
        price = request.form.get('price')
        
        # LEARNING: Basic validation - check if all fields are provided
        if market_id and crop_id and price:
            try:
                # LEARNING: Convert price to float (decimal number)
                price_float = float(price)
                add_price(int(market_id), int(crop_id), price_float)
                # LEARNING: redirect() sends user to a different page
                return redirect(url_for('index'))
            except ValueError:
                # LEARNING: Handle invalid input gracefully
                pass
    
    # LEARNING: For GET requests, show the form with markets and crops
    markets = get_markets()
    crops = get_crops()
    return render_template('add_price.html', markets=markets, crops=crops)

# LEARNING: API endpoint - returns JSON data instead of HTML
# This allows other apps (mobile, React) to use our data
@app.route('/api/prices')
def api_prices():
    """API endpoint to get prices as JSON."""
    prices = get_all_prices()
    
    # LEARNING: Convert database rows to dictionaries for JSON
    prices_list = []
    for price in prices:
        prices_list.append({
            'id': price['id'],
            'market': price['market_name'],
            'location': price['location'],
            'crop': price['crop_name'],
            'category': price['category'],
            'unit': price['unit'],
            'price': price['price'],
            'recorded_at': price['recorded_at']
        })
    
    # LEARNING: jsonify() converts Python dictionary to JSON response
    return jsonify(prices_list)

# LEARNING: Run the application
# debug=True shows detailed error messages (don't use in production!)
if __name__ == '__main__':
    # LEARNING: Initialize database when app starts
    init_database()
    seed_sample_data()
    
    # LEARNING: Start the Flask development server
    # host='0.0.0.0' makes it accessible from other devices on the network
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Step 4: HTML Template (templates/index.html)

```html
<!-- templates/index.html - Main page template -->
<!-- LEARNING: This is a Jinja2 template (Flask's template engine) -->
<!-- It allows us to mix HTML with Python-like logic -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kenya Market Prices</title>
    <!-- LEARNING: link tag connects our CSS file for styling -->
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>🌾 Kenya Market Prices</h1>
            <p class="subtitle">Real-time crop prices across Nairobi markets</p>
        </header>

        <!-- LEARNING: Navigation links -->
        <nav>
            <a href="/" class="nav-link active">All Prices</a>
            <a href="/add-price" class="nav-link">Add Price</a>
            <a href="/api/prices" class="nav-link" target="_blank">API</a>
        </nav>

        <!-- LEARNING: Filter section -->
        <div class="filter-section">
            <form action="/prices" method="GET">
                <input type="text" name="crop" placeholder="Filter by crop (e.g., tomatoes)" 
                       value="{{ filter if filter else '' }}">
                <button type="submit">Search</button>
            </form>
        </div>

        <!-- LEARNING: Price table -->
        <div class="price-table">
            <table>
                <thead>
                    <tr>
                        <th>Market</th>
                        <th>Location</th>
                        <th>Crop</th>
                        <th>Category</th>
                        <th>Price (KES)</th>
                        <th>Unit</th>
                        <th>Recorded</th>
                    </tr>
                </thead>
                <tbody>
                    <!-- LEARNING: Jinja2 for loop - iterates through prices -->
                    <!-- The {% %} syntax is for Python logic -->
                    <!-- The {{ }} syntax is for outputting variables -->
                    {% for price in prices %}
                    <tr>
                        <td>{{ price.market_name }}</td>
                        <td>{{ price.location }}</td>
                        <td>{{ price.crop_name }}</td>
                        <td>{{ price.category }}</td>
                        <td class="price">{{ price.price }}</td>
                        <td>{{ price.unit }}</td>
                        <td>{{ price.recorded_at }}</td>
                    </tr>
                    {% endfor %}
                    
                    <!-- LEARNING: Conditional - show message if no prices -->
                    {% if not prices %}
                    <tr>
                        <td colspan="7" class="no-data">No prices found</td>
                    </tr>
                    {% endif %}
                </tbody>
            </table>
        </div>

        <!-- LEARNING: Summary statistics -->
        <div class="stats">
            <div class="stat-card">
                <h3>Total Entries</h3>
                <p>{{ prices|length }}</p>
            </div>
            <div class="stat-card">
                <h3>Markets</h3>
                <p>{{ prices|map(attribute='market_name')|unique|list|length }}</p>
            </div>
        </div>

        <footer>
            <p>Built with Python, Flask, and SQLite</p>
            <p>Helping Kenyan farmers get fair prices</p>
        </footer>
    </div>
</body>
</html>
```

### Step 5: Add Price Form (templates/add_price.html)

```html
<!-- templates/add_price.html - Form to add new price entries -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Price - Kenya Market Prices</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <header>
            <h1>🌾 Add New Price</h1>
            <p class="subtitle">Record current market prices</p>
        </header>

        <nav>
            <a href="/" class="nav-link">All Prices</a>
            <a href="/add-price" class="nav-link active">Add Price</a>
        </nav>

        <!-- LEARNING: HTML form for data entry -->
        <!-- action="/add-price" sends form to our Flask route -->
        <!-- method="POST" sends data securely (not in URL) -->
        <div class="form-container">
            <form action="/add-price" method="POST">
                <!-- LEARNING: Each form field has a name attribute -->
                <!-- This name is used to access the data in Flask -->
                
                <div class="form-group">
                    <label for="market_id">Market:</label>
                    <!-- LEARNING: <select> creates a dropdown menu -->
                    <select name="market_id" id="market_id" required>
                        <option value="">Select a market</option>
                        <!-- LEARNING: Jinja2 loop to populate dropdown -->
                        {% for market in markets %}
                        <option value="{{ market.id }}">{{ market.name }} - {{ market.location }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="form-group">
                    <label for="crop_id">Crop:</label>
                    <select name="crop_id" id="crop_id" required>
                        <option value="">Select a crop</option>
                        {% for crop in crops %}
                        <option value="{{ crop.id }}">{{ crop.name }} ({{ crop.unit }})</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="form-group">
                    <label for="price">Price (KES):</label>
                    <!-- LEARNING: type="number" allows only numbers -->
                    <!-- step="0.01" allows decimal places -->
                    <input type="number" name="price" id="price" 
                           step="0.01" min="0" required
                           placeholder="Enter price in KES">
                </div>

                <!-- LEARNING: Required attribute ensures field is filled before submit -->
                <button type="submit" class="submit-btn">Add Price</button>
            </form>
        </div>

        <footer>
            <p>Built with Python, Flask, and SQLite</p>
        </footer>
    </div>
</body>
</html>
```

### Step 6: CSS Styling (static/style.css)

```css
/* static/style.css - Styling for the application */
/* LEARNING: CSS (Cascading Style Sheets) controls the visual appearance */
/* Each selector targets HTML elements and applies styles */

/* LEARNING: CSS Reset - removes default browser styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* LEARNING: Body styling - sets the overall page appearance */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f4f4f4;
}

/* LEARNING: Container centers content and limits width */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* LEARNING: Header styling with gradient background */
header {
    background: linear-gradient(135deg, #2d5016 0%, #4a7c23 100%);
    color: white;
    padding: 30px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
}

header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
}

.subtitle {
    opacity: 0.9;
    font-size: 1.1em;
}

/* LEARNING: Navigation styling */
nav {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    justify-content: center;
}

.nav-link {
    padding: 10px 20px;
    background: #fff;
    color: #2d5016;
    text-decoration: none;
    border-radius: 5px;
    transition: all 0.3s ease;
}

.nav-link:hover {
    background: #2d5016;
    color: white;
}

.nav-link.active {
    background: #2d5016;
    color: white;
}

/* LEARNING: Filter section styling */
.filter-section {
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.filter-section form {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.filter-section input {
    flex: 1;
    min-width: 200px;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

.filter-section button {
    padding: 12px 30px;
    background: #4a7c23;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
}

.filter-section button:hover {
    background: #2d5016;
}

/* LEARNING: Table styling */
.price-table {
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

th, td {
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
}

th {
    background: #2d5016;
    color: white;
    font-weight: 600;
}

tr:hover {
    background: #f9f9f9;
}

.price {
    font-weight: bold;
    color: #2d5016;
}

.no-data {
    text-align: center;
    padding: 40px;
    color: #666;
}

/* LEARNING: Statistics cards */
.stats {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 20px;
}

.stat-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.stat-card h3 {
    color: #666;
    font-size: 0.9em;
    margin-bottom: 10px;
}

.stat-card p {
    font-size: 2em;
    color: #2d5016;
    font-weight: bold;
}

/* LEARNING: Form styling */
.form-container {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    max-width: 500px;
    margin: 0 auto;
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #333;
}

.form-group input,
.form-group select {
    width: 100%;
    padding: 12px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}

.form-group input:focus,
.form-group select:focus {
    outline: none;
    border-color: #4a7c23;
    box-shadow: 0 0 5px rgba(74, 124, 35, 0.3);
}

.submit-btn {
    width: 100%;
    padding: 15px;
    background: #4a7c23;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 18px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.submit-btn:hover {
    background: #2d5016;
}

/* LEARNING: Footer styling */
footer {
    text-align: center;
    padding: 20px;
    color: #666;
    border-top: 1px solid #ddd;
    margin-top: 30px;
}

/* LEARNING: Responsive design - adjusts layout for mobile devices */
@media (max-width: 768px) {
    header h1 {
        font-size: 1.8em;
    }
    
    nav {
        flex-direction: column;
    }
    
    .filter-section form {
        flex-direction: column;
    }
    
    table {
        font-size: 14px;
    }
    
    th, td {
        padding: 10px;
    }
}
```

### Step 7: Requirements File (requirements.txt)

```
# requirements.txt - Lists Python packages needed for this project
# LEARNING: pip install -r requirements.txt installs all these packages
# This makes it easy for others to set up the project

Flask==3.0.0
```

---

## Phase 4: Testing & Running

### Step 1: Install Dependencies
```bash
# Open terminal in the project folder
# LEARNING: pip is Python's package manager
# -r reads the requirements file
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
# LEARNING: python runs the Python interpreter
# app.py is our main file
python app.py
```

### Step 3: Open in Browser
- Go to: `http://localhost:5000`
- You should see the market prices page
- Try adding a new price via the form
- Check the API at: `http://localhost:5000/api/prices`

### Step 4: Test Features
1. View all prices on the home page
2. Filter by crop name (try "tomatoes")
3. Add a new price entry
4. Check the API returns JSON data
5. Test on mobile (responsive design)

---

## Phase 5: Next Steps

### Feature Extensions
1. **User Authentication** - Let users create accounts
2. **Price History** - Track price changes over time
3. **Charts** - Visualize price trends with graphs
4. **SMS Alerts** - Notify farmers when prices are favorable
5. **Multi-language** - Add Swahili support

### Deployment to Railway
1. Create account at railway.app
2. Connect your GitHub repository
3. Railway auto-detects Python and deploys
4. Get a public URL to share

### Portfolio Presentation
- Screenshot the app in use
- Explain the problem it solves
- Show the code structure
- Link to live demo
- Mention technologies used

### Monetization Ideas
1. **Subscription** - Charge farmers for premium features
2. **Partnerships** - Work with agricultural cooperatives
3. **API Access** - Sell data access to businesses
4. **Advertising** - Show ads for farm supplies

---

## Learning Exercises

### Exercise 1: Add a New Market
Try adding a new market to the database:
```python
# Add this function to database.py
def add_market(name, location):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO markets (name, location) VALUES (?, ?)",
        (name, location)
    )
    conn.commit()
    conn.close()
```

### Exercise 2: Add Price Comparison
Create a function that compares prices across markets:
```python
def compare_prices(crop_name):
    """Find cheapest and most expensive markets for a crop."""
    prices = get_prices_by_crop(crop_name)
    if not prices:
        return None
    
    cheapest = min(prices, key=lambda x: x['price'])
    expensive = max(prices, key=lambda x: x['price'])
    
    return {
        'crop': crop_name,
        'cheapest_market': cheapest['market_name'],
        'cheapest_price': cheapest['price'],
        'expensive_market': expensive['market_name'],
        'expensive_price': expensive['price'],
        'potential_saving': expensive['price'] - cheapest['price']
    }
```

### Exercise 3: Add Search Feature
Enhance the search to work across all fields:
```python
def search_prices(query):
    """Search prices by market, crop, or location."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM prices p
        JOIN markets m ON p.market_id = m.id
        JOIN crops c ON p.crop_id = c.id
        WHERE m.name LIKE ? 
           OR m.location LIKE ?
           OR c.name LIKE ?
        ORDER BY p.recorded_at DESC
    ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
    
    results = cursor.fetchall()
    conn.close()
    return results
```

---

## Congratulations! 🎉

You've completed your first project! You now have:
- ✅ A working web application
- ✅ Experience with Python and Flask
- ✅ SQL database knowledge
- ✅ HTML/CSS skills
- ✅ REST API understanding
- ✅ A portfolio project

**Next Project:** Healthcare Appointment Booking (Project 2)
