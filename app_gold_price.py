"""
Gold Price API Flask Application
Integration example for serving live gold prices on your website.
"""

from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
from wan.gold_api import GoldPriceAPI
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-domain requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/api/gold-price", methods=["GET"])
def get_gold_price():
    """
    GET /api/gold-price
    Returns current gold price in Omani Rial (OMR)
    
    Response:
    {
        "currency": "OMR",
        "price_per_gram": 1.234,
        "price_per_ounce": 38.45,
        "timestamp": "2024-01-15T10:30:45.123456",
        "usd_to_omr_rate": 0.385,
        "source": "metals.live + exchangerate-api",
        "status": "success"
    }
    """
    try:
        price_data = GoldPriceAPI.get_gold_price_oman()
        logger.info(f"Gold price fetched: {price_data}")
        
        status_code = 200 if price_data.get("status") == "success" else 503
        return jsonify(price_data), status_code
    
    except Exception as e:
        logger.error(f"Error fetching gold price: {e}")
        return jsonify({
            "error": str(e),
            "status": "failed"
        }), 500


@app.route("/api/gold-price/live", methods=["GET"])
def get_gold_price_live():
    """
    Real-time endpoint (can be used for WebSocket in future)
    Same as /api/gold-price but with cache headers disabled
    """
    response = get_gold_price()
    if isinstance(response, tuple):
        data, status = response
        response = jsonify(data)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.status_code = status
    return response


@app.route("/", methods=["GET"])
def index():
    """Simple HTML page to display gold prices"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Live Gold Prices - Oman</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
            }
            .container {
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            h1 {
                color: #764ba2;
                text-align: center;
            }
            .price-display {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
            }
            .price-item {
                display: flex;
                justify-content: space-between;
                margin: 10px 0;
                font-size: 18px;
            }
            .label {
                font-weight: bold;
                color: #764ba2;
            }
            .value {
                color: #27ae60;
                font-weight: bold;
            }
            .timestamp {
                text-align: center;
                color: #7f8c8d;
                font-size: 12px;
                margin-top: 20px;
            }
            .error {
                background: #fadbd8;
                color: #c0392b;
                padding: 15px;
                border-radius: 5px;
                display: none;
            }
            .loading {
                text-align: center;
                color: #667eea;
                font-size: 14px;
            }
            button {
                background: #667eea;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 14px;
                width: 100%;
                margin-top: 20px;
            }
            button:hover {
                background: #764ba2;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>💰 Live Gold Prices</h1>
            <p style="text-align: center; color: #7f8c8d;">Accurate to Oman Market</p>
            
            <div class="loading" id="loading">Loading prices...</div>
            <div class="error" id="error"></div>
            
            <div class="price-display" id="priceDisplay">
                <div class="price-item">
                    <span class="label">Price per Gram:</span>
                    <span class="value" id="priceGram">-</span>
                </div>
                <div class="price-item">
                    <span class="label">Price per Ounce:</span>
                    <span class="value" id="priceOunce">-</span>
                </div>
                <div class="price-item">
                    <span class="label">Currency:</span>
                    <span class="value" id="currency">-</span>
                </div>
                <div class="price-item">
                    <span class="label">USD → OMR Rate:</span>
                    <span class="value" id="rate">-</span>
                </div>
                <div class="timestamp" id="timestamp">Last updated: -</div>
            </div>
            
            <button onclick="fetchGoldPrice()">Refresh Prices</button>
        </div>

        <script>
            function fetchGoldPrice() {
                const loading = document.getElementById('loading');
                const error = document.getElementById('error');
                const display = document.getElementById('priceDisplay');
                
                loading.style.display = 'block';
                error.style.display = 'none';
                
                fetch('/api/gold-price')
                    .then(response => response.json())
                    .then(data => {
                        loading.style.display = 'none';
                        
                        if (data.status === 'success') {
                            document.getElementById('priceGram').textContent = 
                                data.price_per_gram + ' OMR';
                            document.getElementById('priceOunce').textContent = 
                                data.price_per_ounce + ' OMR';
                            document.getElementById('currency').textContent = 
                                data.currency;
                            document.getElementById('rate').textContent = 
                                data.usd_to_omr_rate.toFixed(3);
                            document.getElementById('timestamp').textContent = 
                                'Last updated: ' + new Date(data.timestamp).toLocaleString();
                            display.style.display = 'block';
                        } else {
                            showError(data.error || 'Failed to fetch gold price');
                        }
                    })
                    .catch(err => {
                        loading.style.display = 'none';
                        showError('Network error: ' + err.message);
                    });
            }
            
            function showError(message) {
                document.getElementById('error').textContent = message;
                document.getElementById('error').style.display = 'block';
                document.getElementById('priceDisplay').style.display = 'none';
            }
            
            // Fetch prices on page load
            window.onload = fetchGoldPrice;
            
            // Refresh every 5 minutes (300000 ms)
            setInterval(fetchGoldPrice, 300000);
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    print("Starting Gold Price API server...")
    print("API Endpoint: http://localhost:5000/api/gold-price")
    print("Website: http://localhost:5000/")
    app.run(debug=True, host="0.0.0.0", port=5000)
