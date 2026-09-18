"""
Gold Price API Integrator - Multiple Free & Paid Options for Oman Pricing
Provides complete setup with API keys and configurations for accurate Oman rates
"""

import os
import json

class GoldAPISolutions:
    """
    Complete guide to gold price APIs with Oman-accurate pricing.
    Choose one that works best for your needs.
    """
    
    SOLUTIONS = {
        "1_metals_live_free": {
            "name": "Metals.Live (Free - Recommended for Spot)",
            "endpoint": "https://api.metals.live/v1/spot/gold",
            "api_key": "NOT_REQUIRED",
            "currency": "USD",
            "unit": "USD/gram",
            "pros": [
                "No API key needed",
                "Real-time spot prices",
                "Very reliable",
                "Free tier unlimited",
            ],
            "cons": [
                "Global spot only (no Oman premium included)",
                "May have SSL issues in some environments",
            ],
            "response_format": {"gold": 85.20},
            "oman_adjustment": "Apply 2.14x multiplier for Oman retail (1700 OMR/oz)",
            "setup": "No setup needed - use directly",
            "code_example": """
            import requests
            response = requests.get('https://api.metals.live/v1/spot/gold')
            data = response.json()
            usd_per_gram = data['gold']
            oman_retail_per_gram = usd_per_gram * 0.385 * 2.14  # USD to OMR with premium
            """
        },
        
        "2_goldapi_io_free": {
            "name": "GoldAPI.io (Free Tier - Recommended)",
            "endpoint": "https://www.goldapi.io/api/XAU/USD",
            "api_key": "FREE",
            "description": "Sign up at https://www.goldapi.io/ to get free API key",
            "currency": "USD",
            "unit": "USD per troy ounce",
            "pros": [
                "Very reliable",
                "Free tier: 100 calls/month",
                "Per-ounce prices (matches market standard)",
                "Support for multiple currencies including OMR",
                "Works globally",
            ],
            "cons": [
                "Requires free registration for API key",
                "Limited to 100 calls/month on free tier",
            ],
            "response_format": {
                "status": "success",
                "data": {
                    "xau_usd": 2500.0
                }
            },
            "oman_adjustment": "2.14x multiplier or request OMR directly",
            "setup": """
            1. Go to https://www.goldapi.io/
            2. Sign up for free account
            3. Get your API key from dashboard
            4. Set environment: export GOLDAPI_KEY=your_key_here
            5. Use endpoint: https://www.goldapi.io/api/XAU/OMR?api_key=YOUR_KEY
            """,
            "code_example": """
            import requests
            api_key = os.getenv("GOLDAPI_KEY")
            url = f"https://www.goldapi.io/api/XAU/OMR?api_key={api_key}"
            response = requests.get(url)
            data = response.json()
            omr_per_ounce = data['data']['xau_omr']
            omr_per_gram = omr_per_ounce / 31.1035
            """
        },
        
        "3_metal_quotes_paid": {
            "name": "MetalQuotes API (Paid - High Accuracy)",
            "endpoint": "https://api.metalquotes.com/gold",
            "api_key": "PAID_SUBSCRIPTION",
            "currency": "Multiple (includes OMR)",
            "pros": [
                "Highest accuracy",
                "Real-time + historical data",
                "Oman-specific rates available",
                "Excellent support",
                "Multiple currency support",
            ],
            "cons": [
                "Requires paid subscription ($29+/month)",
                "Overkill for basic price display",
            ],
            "setup": "Sign up at https://www.metalquotes.com/",
            "documentation": "https://www.metalquotes.com/documentation"
        },
        
        "4_xe_currency_free": {
            "name": "XE.com Currency (Free - For USD→OMR Conversion)",
            "endpoint": "https://xe.com/currency_charts/XAU_OMR",
            "api_key": "NOT_REQUIRED",
            "approach": "Web scraping (less ideal)",
            "pros": [
                "Free",
                "Direct OMR conversion",
                "Real-time rates",
            ],
            "cons": [
                "Requires web scraping (fragile)",
                "May violate ToS",
                "Slower than API",
            ],
            "note": "Not recommended - use with GoldAPI instead"
        },
        
        "5_oman_central_bank": {
            "name": "Oman Central Bank (Most Accurate Local)",
            "info": "Official Oman exchange rates and gold pricing",
            "website": "https://www.cbo.gov.om/",
            "approach": "Contact or web scraping",
            "pros": [
                "Official source",
                "Most accurate for Oman",
                "Authoritative rates",
            ],
            "cons": [
                "No public API",
                "Requires web scraping",
                "Updates may be daily only",
            ],
            "recommendation": "Check website for official gold rates",
            "note": "Could combine with GoldAPI.io for real-time + official rates"
        }
    }

    @staticmethod
    def print_solutions():
        """Print all available solutions"""
        print("\n" + "="*80)
        print("COMPLETE GOLD API SOLUTIONS FOR OMAN PRICING")
        print("="*80 + "\n")
        
        for key, solution in GoldAPISolutions.SOLUTIONS.items():
            print(f"\n{key.upper()}")
            print("-" * 60)
            print(f"Name: {solution.get('name')}")
            print(f"API Key: {solution.get('api_key', 'N/A')}")
            print(f"Endpoint: {solution.get('endpoint', 'N/A')}")
            
            if solution.get('pros'):
                print(f"\nPros:")
                for pro in solution['pros']:
                    print(f"  ✓ {pro}")
            
            if solution.get('cons'):
                print(f"\nCons:")
                for con in solution['cons']:
                    print(f"  ✗ {con}")
            
            if solution.get('setup'):
                print(f"\nSetup:\n{solution['setup']}")
            
            if solution.get('code_example'):
                print(f"\nCode Example:{solution['code_example']}")
            
            print()

    @staticmethod
    def get_recommended_setup():
        """Get recommended setup for Oman gold prices"""
        return {
            "primary": "GoldAPI.io (Free - Recommended)",
            "backup": "Metals.Live with 2.14x multiplier",
            "official": "Oman Central Bank for verification",
            
            "implementation": """
RECOMMENDED SETUP:
================
1. Use GoldAPI.io with OMR currency
   - Free tier: https://www.goldapi.io/
   - Sign up for API key
   - Request XAU/OMR directly (Oman pricing included)
   - 100 calls/month free (enough for daily updates)

2. Update your Python code:

   from wan.gold_api import GoldPriceAPI
   
   # Set environment variable:
   export GOLDAPI_KEY=your_api_key_from_goldapi_io
   
   # The API will use this key automatically

3. Deploy with:
   
   export GOLD_PRICE_API_PROVIDER=goldapi_io
   export GOLDAPI_KEY=your_key_here
   python app_gold_price.py

ALTERNATIVE (If GoldAPI.io not working):
=========================================
1. Use Metals.Live (no key needed)
2. Set Oman retail multiplier:
   export GOLD_PRICE_PREMIUM_MULTIPLIER=2.14
   python app_gold_price.py

3. Manually update spot price when it changes:
   export GOLD_PRICE_FALLBACK_USD_OZ=4400
   python app_gold_price.py
            """
        }


if __name__ == "__main__":
    GoldAPISolutions.print_solutions()
    
    print("\n" + "="*80)
    print("RECOMMENDED SOLUTION")
    print("="*80)
    rec = GoldAPISolutions.get_recommended_setup()
    print(f"\nPrimary: {rec['primary']}")
    print(f"Backup: {rec['backup']}")
    print(f"Official: {rec['official']}")
    print(f"\n{rec['implementation']}")
