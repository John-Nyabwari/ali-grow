from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import init_database, seed_sample_data, get_all_prices, get_prices_by_crop, add_price, get_markets, get_crops

# Create Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """Home page - display all prices."""
    prices = get_all_prices()
    return render_template('index.html', prices=prices)

@app.route('/prices')
def prices_page():
    """Prices page with filtering."""
    crop_filter = request.args.get('crop', '')
    
    if crop_filter:
        prices = get_prices_by_crop(crop_filter)
    else:
        prices = get_all_prices()
    
    return render_template('index.html', prices=prices, filter=crop_filter)

@app.route('/add_price', methods=['GET', 'POST'])
def add_price_page():
    """Page to add new price entries."""
    if request.method == 'POST':
        market_id = request.form['market_id']
        crop_id = request.form['crop_id']
        price = request.form['price']
        
        if market_id and crop_id and price:
            try:
                price_float = float(price)
                add_price(int(market_id), int(crop_id), price_float)
                return redirect(url_for('index'))
            except ValueError:
                pass
    
    markets = get_markets()
    crops = get_crops()
    return render_template('add_price.html', markets=markets, crops=crops)

@app.route('/api/prices')
def api_prices():
    """API endpoint to get prices in JSON format."""
    prices = get_all_prices()
    
    price_list = []
    
    for price in prices:
        price_list.append({
            'id': price['id'],
            'market_name': price['market_name'],
            'location': price['location'],
            'crop_name': price['crop_name'],
            'category': price['category'],
            'unit': price['unit'],
            'price': price['price'],
            'recorded_at': price['recorded_at']
        })
    
    return jsonify(price_list)

# Run the application
if __name__ == '__main__':
    # Initialize database and add sample data
    init_database()
    seed_sample_data()
    
    # Start the Flask development server
    # debug=True shows detailed errors (remove in production)
    # host='0.0.0.0' makes it accessible from other devices
    app.run(debug=True, host='0.0.0.0', port=5000)
