"""
Gold Price API - Oman Market Edition with Multi-Provider Support
Fetches live gold prices with multi-purity support (24K, 22K, 21K, 18K).
Supports: GoldAPI.io (OMR), Metals.Live (USD), and custom fallback.

SETUP INSTRUCTIONS:
===================
Option 1 - GoldAPI.io (Recommended - Direct OMR Support):
  1. Sign up at https://www.goldapi.io/ (free tier: 100 calls/month)
  2. Get your API key
  3. Set environment: export GOLDAPI_KEY=your_key_here
  4. Run: python app_gold_price.py

Option 2 - Metals.Live (No API Key Needed):
  1. Set premium multiplier: export GOLD_PRICE_PREMIUM_MULTIPLIER=2.14
  2. Set spot price: export GOLD_PRICE_FALLBACK_USD_OZ=2500.0
  3. Run: python app_gold_price.py

Option 3 - Custom Manual Price:
  1. Set: export GOLD_PRICE_FALLBACK_USD_OZ=4400.0
  2. Run: python app_gold_price.py
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Optional

class GoldPriceAPI:
    """Fetch live gold prices with multi-provider support for Oman."""
    
    # APIs
    METALS_LIVE_API = "https://api.metals.live/v1/spot/gold"
    GOLDAPI_IO_BASE = "https://www.goldapi.io/api/XAU"
    CURRENCY_CONVERT_URL = "https://api.exchangerate-api.com/v4/latest/USD"
    
    # Configuration from environment variables
    GOLDAPI_KEY = os.getenv("GOLDAPI_KEY", "")
    DEFAULT_PREMIUM = float(os.getenv("GOLD_PRICE_PREMIUM_MULTIPLIER", "2.14"))
    DEFAULT_FALLBACK_USD_OZ = float(os.getenv("GOLD_PRICE_FALLBACK_USD_OZ", "2500.0"))
    
    @staticmethod
    def get_gold_price_from_goldapi_io() -> Optional[Dict]:
        """
        Fetch gold price from GoldAPI.io with OMR support.
        Best option - Direct Oman Rial pricing included.
        Free tier: 100 calls/month (enough for ~3 calls/day)
        """
        if not GoldPriceAPI.GOLDAPI_KEY:
            return None
        
        try:
            # Request OMR price (Oman Rial)
            url = f"{GoldPriceAPI.GOLDAPI_IO_BASE}/OMR?api_key={GoldPriceAPI.GOLDAPI_KEY}"
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success" and "data" in data:
                price_omr_oz = data["data"].get("xau_omr")
                print(f"[SUCCESS] GoldAPI.io: {price_omr_oz} OMR/oz")
                
                if price_omr_oz and price_omr_oz > 100:  # Sanity check
                    return {
                        "price_omr_per_oz": price_omr_oz,
                        "price_omr_per_gram": price_omr_oz / 31.1035,
                        "timestamp": datetime.utcnow().isoformat(),
                        "source": "goldapi_io_omr",
                        "already_in_omr": True
                    }
        except Exception as e:
            print(f"[ERROR] GoldAPI.io failed: {str(e)[:100]}")
        
        return None
    
    @staticmethod
    def get_gold_price_usd() -> Optional[Dict]:
        """
        Fetch gold price in USD (fallback if OMR not available).
        Returns price in USD per gram.
        """
        try:
            response = requests.get(GoldPriceAPI.METALS_LIVE_API, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            
            price_usd_per_gram = data.get("gold")
            print(f"[DEBUG] Metals.Live: {price_usd_per_gram} USD/gram")
            
            if price_usd_per_gram and price_usd_per_gram > 50:
                return {
                    "price_usd_per_gram": price_usd_per_gram,
                    "price_usd_per_oz": price_usd_per_gram * 31.1035,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "metals_live",
                }
        except Exception as e:
            print(f"[ERROR] Metals.Live failed: {str(e)[:100]}")
        
        # Fallback: Hardcoded price (update GOLD_PRICE_FALLBACK_USD_OZ environment variable)
        fallback_usd_per_oz = GoldPriceAPI.DEFAULT_FALLBACK_USD_OZ
        fallback_usd_per_gram = fallback_usd_per_oz / 31.1035
        
        print(f"[FALLBACK] Using: ${fallback_usd_per_oz}/oz (${fallback_usd_per_gram:.2f}/gram)")
        print(f"[FALLBACK] Update with: export GOLD_PRICE_FALLBACK_USD_OZ=new_price")
        
        return {
            "price_usd_per_gram": fallback_usd_per_gram,
            "price_usd_per_oz": fallback_usd_per_oz,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "fallback_approximation",
            "note": "Not live data - update GOLD_PRICE_FALLBACK_USD_OZ when prices change"
        }
    
    @staticmethod
    def get_usd_to_omr_rate() -> float:
        """Fetch current USD to OMR exchange rate."""
        try:
            response = requests.get(GoldPriceAPI.CURRENCY_CONVERT_URL, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            omr_rate = data.get("rates", {}).get("OMR")
            if omr_rate:
                print(f"[DEBUG] Exchange rate: 1 USD = {omr_rate} OMR")
                return omr_rate
        except Exception as e:
            print(f"[ERROR] Exchange rate fetch failed: {str(e)[:80]}")
        
        # Oman Rial is pegged to USD at 1 USD = 0.385 OMR (official, very stable)
        print(f"[FALLBACK] Using official rate: 1 USD = 0.385 OMR")
        return 0.385
    
    @staticmethod
    def calculate_purity_prices(price_24k: float) -> Dict[str, float]:
        """
        Calculate prices for different purities (24K, 22K, 21K, 18K).
        Gold purity percentages:
        - 24K = 100% pure
        - 22K = 91.67% pure (22/24)
        - 21K = 87.5% pure (21/24)
        - 18K = 75% pure (18/24)
        """
        return {
            "24K": round(price_24k, 3),
            "22K": round(price_24k * 22/24, 3),
            "21K": round(price_24k * 21/24, 3),
            "18K": round(price_24k * 18/24, 3),
        }
    
    @staticmethod
    def get_gold_price_oman(premium_multiplier: Optional[float] = None) -> Dict:
        """
        Get current gold prices in Omani Rial (OMR).
        
        Priority:
        1. Try GoldAPI.io (direct OMR if key available)
        2. Fall back to Metals.Live + USD→OMR conversion
        3. Use hardcoded fallback if all else fails
        
        Args:
            premium_multiplier: Apply retail/local premium to USD spot prices.
                               Only used if not getting OMR from GoldAPI.io.
                               Default: 2.14x for Oman retail.
        """
        
        # Try GoldAPI.io first (best option - direct OMR)
        print("\n[STEP 1] Checking GoldAPI.io (OMR)...")
        goldapi_data = GoldPriceAPI.get_gold_price_from_goldapi_io()
        
        if goldapi_data and goldapi_data.get("price_omr_per_gram"):
            # Got OMR directly from GoldAPI.io - no need for premium multiplier
            price_omr_gram_24k = goldapi_data["price_omr_per_gram"]
            price_omr_oz_24k = goldapi_data["price_omr_per_oz"]
            source = "GoldAPI.io (Direct OMR)"
            price_type = "Oman Market"
            premium_used = None
        
        else:
            # Fall back to USD conversion with premium
            print("\n[STEP 2] Falling back to USD conversion...")
            
            usd_data = GoldPriceAPI.get_gold_price_usd()
            omr_rate = GoldPriceAPI.get_usd_to_omr_rate()
            
            # Convert USD to OMR
            price_usd_gram = usd_data["price_usd_per_gram"]
            price_omr_gram_24k_spot = price_usd_gram * omr_rate
            price_omr_oz_24k_spot = price_omr_gram_24k_spot * 31.1035
            
            # Apply premium if specified
            if premium_multiplier is None:
                premium_multiplier = GoldPriceAPI.DEFAULT_PREMIUM
            
            if premium_multiplier != 1.0:
                price_omr_gram_24k = price_omr_gram_24k_spot * premium_multiplier
                price_omr_oz_24k = price_omr_oz_24k_spot * premium_multiplier
                price_type = "Oman Retail"
                premium_used = premium_multiplier
            else:
                price_omr_gram_24k = price_omr_gram_24k_spot
                price_omr_oz_24k = price_omr_oz_24k_spot
                price_type = "Global Spot"
                premium_used = None
            
            source = usd_data.get("source", "unknown")
            goldapi_data = usd_data
        
        # Calculate purity breakdown
        purity_prices_gram = GoldPriceAPI.calculate_purity_prices(price_omr_gram_24k)
        purity_prices_oz = GoldPriceAPI.calculate_purity_prices(price_omr_oz_24k)
        
        response = {
            "currency": "OMR",
            "price_type": price_type,
            "purity_base": "24K (pure gold)",
            "timestamp": goldapi_data.get("timestamp", datetime.utcnow().isoformat()),
            "source": source,
            "usd_to_omr_rate": GoldPriceAPI.get_usd_to_omr_rate(),
            "status": "success",
            
            # Per gram prices (all purities)
            "per_gram": purity_prices_gram,
            "per_gram_unit": "OMR/gram",
            
            # Per troy ounce prices (all purities)
            "per_oz": purity_prices_oz,
            "per_oz_unit": "OMR/troy ounce",
            
            # Legacy fields
            "price_per_gram": price_omr_gram_24k,
            "price_per_ounce": price_omr_oz_24k,
            
            # Metadata
            "metadata": {
                "note": "All prices in 24K pure gold. Use per_gram/per_oz for purity-specific prices.",
                "price_type_note": f"Provider: {source}",
            }
        }
        
        if premium_used:
            response["premium_multiplier"] = premium_used
            response["metadata"]["premium_note"] = f"Applied {premium_used}x retail premium to spot price"
        
        return response


def create_gold_price_endpoint(app):
    """Add gold price endpoint to Flask app."""
    @app.route("/api/gold-price", methods=["GET"])
    def gold_price():
        from flask import request
        
        premium_str = request.args.get("premium")
        premium = None
        
        if premium_str:
            try:
                premium = float(premium_str)
                if premium <= 0:
                    return {"error": "Premium must be > 0", "status": "failed"}, 400
            except ValueError:
                return {"error": f"Invalid premium: {premium_str}", "status": "failed"}, 400
        
        price_data = GoldPriceAPI.get_gold_price_oman(premium_multiplier=premium)
        status_code = 200 if price_data.get("status") == "success" else 503
        return price_data, status_code


if __name__ == "__main__":
    # Test the API
    print("="*80)
    print("GOLD PRICE API TEST - Oman Market Edition")
    print("="*80)
    price = GoldPriceAPI.get_gold_price_oman()
    print("\n" + "="*80)
    print("RESULT")
    print("="*80)
    print(json.dumps(price, indent=2))
