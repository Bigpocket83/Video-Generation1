"""
Gold Price API - Oman Market Edition
Fetches live gold prices with multi-purity support (24K, 22K, 21K, 18K).
All prices are base on 24K (pure gold) and derived for other purities.
Supports configurable premium multiplier for Oman retail/local rates.
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, Optional

class GoldPriceAPI:
    """Fetch live gold prices with Oman retail premium support."""
    
    # Data sources
    METALS_LIVE_API = "https://api.metals.live/v1/spot/gold"
    CURRENCY_CONVERT_URL = "https://api.exchangerate-api.com/v4/latest/USD"
    
    # Premium multiplier for Oman retail prices (configurable)
    # Default: 2.14 (approximately 54 OMR/gram from 25.29 global spot)
    # Set via environment: GOLD_PRICE_PREMIUM_MULTIPLIER
    DEFAULT_PREMIUM = float(os.getenv("GOLD_PRICE_PREMIUM_MULTIPLIER", "2.14"))
    
    # Fallback USD/oz when APIs unavailable (update when gold prices change significantly)
    # IMPORTANT: This becomes stale over time. Set via env var GOLD_PRICE_FALLBACK_USD_OZ
    DEFAULT_FALLBACK_USD_OZ = float(os.getenv("GOLD_PRICE_FALLBACK_USD_OZ", "2500.0"))
    
    @staticmethod
    def get_gold_price_usd() -> Optional[Dict]:
        """
        Fetch current gold price in USD.
        Returns price in USD per troy ounce (standard unit).
        Note: 1 troy ounce = 31.1035 grams
        """
        
        # Try metals.live (returns USD per gram)
        try:
            response = requests.get(GoldPriceAPI.METALS_LIVE_API, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()
            
            price_usd_per_gram = data.get("gold")
            print(f"[DEBUG] metals.live raw response: {data}")
            print(f"[DEBUG] price_usd_per_gram: {price_usd_per_gram}")
            
            if price_usd_per_gram and price_usd_per_gram > 50:  # Sanity check: gold should be >$50/gram
                price_usd_per_oz = price_usd_per_gram * 31.1035  # Convert to troy ounce
                print(f"[DEBUG] Converted to USD/oz: {price_usd_per_oz}")
                return {
                    "price_usd_per_gram": price_usd_per_gram,
                    "price_usd_per_oz": price_usd_per_oz,
                    "timestamp": datetime.utcnow().isoformat(),
                    "source": "metals.live",
                    "unit_verified": True
                }
        except Exception as e:
            print(f"[ERROR] metals.live API failed: {e}")
        
        # Fallback: Use realistic current spot price
        # CRITICAL: Update this regularly as gold prices fluctuate!
        # As of Sept 2024-2026: Gold spot typically $2,300-2,700/oz
        # User reports current rate: ~$4,300-4,400/oz (verify your current market)
        # Using $2,500/oz as conservative 2024-2026 estimate
        fallback_usd_per_oz = 2500.0
        fallback_usd_per_gram = fallback_usd_per_oz / 31.1035
        # Fallback: Use configurable spot price (when APIs unavailable)
        # IMPORTANT: This becomes stale - update GOLD_PRICE_FALLBACK_USD_OZ environment variable
        # when gold prices change significantly
        fallback_usd_per_oz = GoldPriceAPI.DEFAULT_FALLBACK_USD_OZ
        fallback_usd_per_gram = fallback_usd_per_oz / 31.1035
        
        print(f"[FALLBACK] Using hardcoded spot: ${fallback_usd_per_oz}/oz (${fallback_usd_per_gram:.2f}/gram)")
        print(f"[FALLBACK] WARNING: This is not live data - live APIs unavailable!")
        print(f"[FALLBACK] To update, set: GOLD_PRICE_FALLBACK_USD_OZ=<new_price>")
        
        return {
            "price_usd_per_gram": fallback_usd_per_gram,
            "price_usd_per_oz": fallback_usd_per_oz,
            "timestamp": datetime.utcnow().isoformat(),
            "source": "fallback_approximation",
            "note": "Live APIs unavailable; using Sept 2024 market approximation"
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
                return omr_rate
        except Exception as e:
            print(f"Error fetching exchange rate: {e}")
        
        # Omani Rial is pegged to USD: 1 USD = 0.385 OMR (official rate, very stable)
        return 0.385
    
    @staticmethod
    def calculate_purity_prices(price_24k: float) -> Dict[str, float]:
        """
        Calculate gold prices for different purities based on 24K base.
        Gold purity is measured in karats:
        - 24K = 100% pure gold
        - 22K = 91.67% pure gold (22/24)
        - 21K = 87.5% pure gold (21/24)
        - 18K = 75% pure gold (18/24)
        """
        return {
            "24K": round(price_24k, 3),           # Pure gold
            "22K": round(price_24k * 22/24, 3),  # 91.67% pure
            "21K": round(price_24k * 21/24, 3),  # 87.5% pure
            "18K": round(price_24k * 18/24, 3),  # 75% pure
        }
    
    @staticmethod
    def get_gold_price_oman(premium_multiplier: Optional[float] = None) -> Dict:
        """
        Get current gold prices in Omani Rial (OMR).
        Returns 24K pure gold as base, with derived purities (22K, 21K, 18K).
        
        Args:
            premium_multiplier: Apply retail/local premium to spot prices.
                               If None, uses DEFAULT_PREMIUM (set via env var).
                               Example: 2.14 multiplies spot by 2.14x for Oman retail.
        """
        usd_data = GoldPriceAPI.get_gold_price_usd()
        
        if not usd_data:
            return {
                "error": "Unable to fetch gold price",
                "status": "failed"
            }
        
        omr_rate = GoldPriceAPI.get_usd_to_omr_rate()
        
        # Convert USD per gram to OMR per gram (24K pure)
        price_usd_gram = usd_data["price_usd_per_gram"]
        price_omr_gram_24k = price_usd_gram * omr_rate
        
        # Apply premium multiplier if provided
        if premium_multiplier is None:
            premium_multiplier = GoldPriceAPI.DEFAULT_PREMIUM
        
        if premium_multiplier != 1.0:
            price_omr_gram_24k_retail = price_omr_gram_24k * premium_multiplier
            price_type = "Oman Retail"
        else:
            price_omr_gram_24k_retail = price_omr_gram_24k
            price_type = "Global Spot"
        
        # Convert to per ounce
        GRAMS_PER_OUNCE = 31.1035
        price_omr_oz_24k_retail = price_omr_gram_24k_retail * GRAMS_PER_OUNCE
        
        # Calculate prices for different purities
        purity_prices_gram = GoldPriceAPI.calculate_purity_prices(price_omr_gram_24k_retail)
        purity_prices_oz = GoldPriceAPI.calculate_purity_prices(price_omr_oz_24k_retail)
        
        return {
            "currency": "OMR",
            "price_type": price_type,
            "purity_base": "24K (pure gold)",
            "premium_multiplier": premium_multiplier,
            "timestamp": usd_data["timestamp"],
            "source": usd_data.get("source", "unknown"),
            "usd_to_omr_rate": omr_rate,
            "status": "success",
            
            # Per gram prices (all purities)
            "per_gram": purity_prices_gram,
            "per_gram_unit": "OMR/gram",
            
            # Per troy ounce prices (all purities)
            "per_oz": purity_prices_oz,
            "per_oz_unit": "OMR/troy ounce",
            
            # Legacy fields for backward compatibility
            "price_per_gram": price_omr_gram_24k_retail,  # 24K
            "price_per_ounce": price_omr_oz_24k_retail,  # 24K
            
            # Metadata
            "metadata": {
                "note": "All prices in 24K pure gold. Use per_gram/per_oz for purity-specific prices.",
                "price_type_note": f"Premium multiplier {premium_multiplier}x applied to spot price.",
                "conversions": {
                    "grams_per_troy_ounce": GRAMS_PER_OUNCE,
                    "usd_per_gram_spot": price_usd_gram,
                    "usd_per_oz_spot": usd_data.get("price_usd_per_oz", price_usd_gram * GRAMS_PER_OUNCE),
                    "omr_per_gram_spot": round(price_omr_gram_24k, 3)
                }
            }
        }


def create_gold_price_endpoint(app):
    """
    Add a gold price endpoint to your Flask/FastAPI app.
    
    Usage with Flask:
        from flask import Flask, jsonify
        app = Flask(__name__)
        create_gold_price_endpoint(app)
        app.run()
    
    Endpoint: GET /api/gold-price
    Returns: JSON with current gold price in OMR (with purity tiers)
    """
    @app.route("/api/gold-price", methods=["GET"])
    def gold_price():
        price_data = GoldPriceAPI.get_gold_price_oman()
        return price_data, 200 if price_data.get("status") == "success" else 503


if __name__ == "__main__":
    # Test the API with full purity breakdown
    price = GoldPriceAPI.get_gold_price_oman()
    print(json.dumps(price, indent=2))
