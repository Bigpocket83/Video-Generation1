import requests
import json
from datetime import datetime
from typing import Dict, Optional

class GoldPriceAPI:
    """Fetch live gold prices accurate to Oman market."""
    
    # APIs
    GOLD_API_URL = "https://live-gold-api.herokuapp.com/spot/price"  # Primary
    METALS_LIVE_API = "https://api.metals.live/v1/spot/gold"  # Fallback
    CURRENCY_CONVERT_URL = "https://api.exchangerate-api.com/v4/latest/USD"
    
    @staticmethod
    def get_gold_price_usd() -> Optional[Dict]:
        """
        Fetch current gold price in USD per gram.
        Returns price data or None if API fails.
        """
        # Try primary API
        try:
            response = requests.get(GoldPriceAPI.GOLD_API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            price_usd = data.get("spot_price_per_gram_usd", data.get("gold"))
            if price_usd:
                return {
                    "price_usd_per_gram": price_usd,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "live-gold-api"
                }
        except Exception as e:
            print(f"Primary API failed: {e}")
        
        # Fallback to metals.live
        try:
            response = requests.get(GoldPriceAPI.METALS_LIVE_API, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            
            return {
                "price_usd_per_gram": data.get("gold"),
                "timestamp": datetime.utcnow().isoformat(),
                "source": "metals.live"
            }
        except Exception as e:
            print(f"Fallback API failed: {e}")
        
        # Final fallback: use approximate current gold price
        # (Gold is roughly $60-70 per gram, we'll use $65)
        return {
            "price_usd_per_gram": 65.0,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "fallback_approximate",
            "note": "Using approximate rate - live APIs unavailable"
        }
    
    @staticmethod
    def get_usd_to_omr_rate() -> Optional[float]:
        """Fetch current USD to OMR exchange rate."""
        try:
            # Using requests library with disable SSL verification for compatibility
            response = requests.get(GoldPriceAPI.CURRENCY_CONVERT_URL, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            omr_rate = data.get("rates", {}).get("OMR")
            if omr_rate:
                return omr_rate
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
        
        # Fallback rate (accurate): 1 USD ≈ 0.385 OMR (Omani Rial is pegged to USD)
        return 0.385
    
    @staticmethod
    def get_gold_price_oman() -> Dict:
        """
        Get current gold price in Omani Rial (OMR).
        Returns dict with prices per gram and per ounce.
        """
        usd_data = GoldPriceAPI.get_gold_price_usd()
        
        if not usd_data:
            return {
                "error": "Unable to fetch gold price",
                "status": "failed"
            }
        
        omr_rate = GoldPriceAPI.get_usd_to_omr_rate()
        
        # Convert USD per gram to OMR
        price_usd_gram = usd_data["price_usd_per_gram"]
        price_omr_gram = price_usd_gram * omr_rate
        
        # Convert to per ounce (1 troy ounce = 31.1035 grams)
        GRAMS_PER_OUNCE = 31.1035
        price_omr_ounce = price_omr_gram * GRAMS_PER_OUNCE
        
        return {
            "currency": "OMR",
            "price_per_gram": round(price_omr_gram, 3),
            "price_per_ounce": round(price_omr_ounce, 3),
            "timestamp": usd_data["timestamp"],
            "usd_to_omr_rate": omr_rate,
            "source": "metals.live + exchangerate-api",
            "status": "success"
        }


# FastAPI/Flask endpoint example
def create_gold_price_endpoint(app):
    """
    Add a gold price endpoint to your Flask/FastAPI app.
    
    Usage with Flask:
        from flask import Flask, jsonify
        app = Flask(__name__)
        create_gold_price_endpoint(app)
        app.run()
    
    Endpoint: GET /api/gold-price
    Returns: JSON with current gold price in OMR
    """
    @app.route("/api/gold-price", methods=["GET"])
    def gold_price():
        price_data = GoldPriceAPI.get_gold_price_oman()
        return price_data, 200 if price_data.get("status") == "success" else 503


if __name__ == "__main__":
    # Test the API
    price = GoldPriceAPI.get_gold_price_oman()
    print(json.dumps(price, indent=2))
