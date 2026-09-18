# Gold Price API for Oman Market

This API provides live gold prices with purity-specific breakdowns (24K, 22K, 21K, 18K), converted to Omani Rial (OMR).

## ⚠️ Pricing Mode: Oman Retail (Default)

**This API now returns Oman retail prices by default** (2.14x multiplier):
- Spot gold global: ~25.29 OMR/gram (786.73 OMR/oz)
- **Oman retail: ~54.13 OMR/gram (1,683.61 OMR/oz)** ✓ Default
- Multiplier accounts for local markup, fabrication, and market conditions

**To get different pricing:**
- Global spot: `?premium=1.0`
- Custom premium: `?premium=2.5`
- Set env var: `GOLD_PRICE_PREMIUM_MULTIPLIER=2.0`

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Gold Price API Server

```bash
python app_gold_price.py
```

Server starts on `http://localhost:5000`

### 3. Access the API

#### Get Gold Prices (JSON API)
```bash
curl http://localhost:5000/api/gold-price
```

**Response (with Oman retail premium):**
```json
{
  "currency": "OMR",
  "price_type": "Oman Retail",
  "purity_base": "24K (pure gold)",
  "premium_multiplier": 2.14,
  "per_gram": {
    "24K": 54.13,
    "22K": 49.62,
    "21K": 47.36,
    "18K": 40.60
  },
  "per_oz": {
    "24K": 1683.61,
    "22K": 1543.31,
    "21K": 1473.16,
    "18K": 1262.71
  },
  "timestamp": "2026-09-18T10:33:41.235160",
  "source": "metals.live",
  "usd_to_omr_rate": 0.384,
  "status": "success"
}
```

#### View Live Dashboard
Open your browser: `http://localhost:5000`

---

## Premium Multiplier: Oman Retail vs. Global Spot

**What is the premium multiplier?**
- Converts global spot price to Oman retail/wholesale rate
- Default: **2.14x** (results in ~54 OMR/gram, matching your market rate)
- This accounts for Oman markup, fabrication, and local market conditions

**How to adjust:**

1. **Global Spot (No Premium):**
   ```bash
   curl 'http://localhost:5000/api/gold-price?premium=1.0'
   ```
   Returns: ~25.29 OMR/gram (pure global rate)

2. **Oman Retail (Default):**
   ```bash
   curl http://localhost:5000/api/gold-price
   ```
   Returns: ~54.13 OMR/gram (2.14x multiplier)

3. **Custom Premium:**
   ```bash
   curl 'http://localhost:5000/api/gold-price?premium=2.5'
   ```

4. **Environment Variable (Persistent):**
   ```bash
   export GOLD_PRICE_PREMIUM_MULTIPLIER=2.14
   python app_gold_price.py
   ```

**Python Usage:**
```python
from wan.gold_api import GoldPriceAPI

# Oman retail (default 2.14x)
prices = GoldPriceAPI.get_gold_price_oman()

# Global spot
prices_spot = GoldPriceAPI.get_gold_price_oman(premium_multiplier=1.0)

# Custom
prices_custom = GoldPriceAPI.get_gold_price_oman(premium_multiplier=2.5)
```

**Response shows:**
```json
{
  "price_type": "Oman Retail",
  "premium_multiplier": 2.14,
  "metadata": {
    "conversions": {
      "omr_per_gram_spot": 25.294  // Global spot before premium
    }
  }
}
```

---

All prices are derived from **24K (pure gold)** as the base:

| Purity | % Pure | Calculation | Use Case |
|--------|--------|-------------|----------|
| **24K** | 100% | Base × 1.00 | Fine gold, bullion |
| **22K** | 91.67% | Base × 22/24 | India, Gulf standard jewelry |
| **21K** | 87.5% | Base × 21/24 | Popular in Middle East/Oman |
| **18K** | 75% | Base × 18/24 | Western jewelry, lighter alloys |

**Example:** If 24K = 25.29 OMR/gram, then:
- 22K = 25.29 × (22/24) = 23.15 OMR/gram
- 21K = 25.29 × (21/24) = 22.08 OMR/gram
- 18K = 25.29 × (18/24) = 18.97 OMR/gram

---

## Integration Examples

### JavaScript (Frontend)

```javascript
// Fetch gold prices with all purities
fetch('/api/gold-price')
  .then(res => res.json())
  .then(data => {
    console.log(`24K: ${data.per_gram['24K']} OMR/gram`);
    console.log(`22K: ${data.per_gram['22K']} OMR/gram`);
    console.log(`21K: ${data.per_gram['21K']} OMR/gram`);
    console.log(`18K: ${data.per_gram['18K']} OMR/gram`);
  });
```

### Python (Backend)

```python
from wan.gold_api import GoldPriceAPI

# Get current gold prices
prices = GoldPriceAPI.get_gold_price_oman()

print(f"24K: {prices['per_gram']['24K']} OMR/gram")
print(f"22K: {prices['per_gram']['22K']} OMR/gram")
print(f"21K: {prices['per_gram']['21K']} OMR/gram")
```

### cURL

```bash
# Get prices
curl http://localhost:5000/api/gold-price

# Real-time endpoint (no caching)
curl http://localhost:5000/api/gold-price/live
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/gold-price` | GET | Get current gold prices (all purities) in OMR |
| `/api/gold-price/live` | GET | Real-time endpoint (no browser cache) |
| `/` | GET | View live dashboard with purity breakdown |

---

## Data Sources & Accuracy

### Current Sources
- **Gold Prices**: metals.live API (international spot price)
- **Exchange Rate**: exchangerate-api.com (USD → OMR, live)
- **Fallback**: Market-based approximation if APIs unavailable

### Formula
```
Price OMR = (Spot Price USD/oz) × (USD→OMR Rate) ÷ 31.1035 × Purity Factor
```

### Important Notes

⚠️ **This API returns GLOBAL SPOT prices**, converted to OMR:
- Does NOT include local Oman premiums, fabrication fees, or retailer margins
- Does NOT track Oman souk or CBE official rates
- Suitable for: Real-time spot tracking, commodity trading, initial quotes
- NOT suitable for: Retail jewelry pricing without local adjustments

**If you need Oman market-specific rates:**
- Consider sourcing from Oman Central Bank or local gold souk APIs
- Add a local premium multiplier (e.g., 1.05 for 5% retail markup)
- We can help integrate if you have access to those feeds

---

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app_gold_price.py"]
```

```bash
docker build -t gold-price-api .
docker run -p 5000:5000 gold-price-api
```

### Production (Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app_gold_price:app
```

---

## Testing

```bash
# Test the API module
python wan/gold_api.py

# Test the Flask app
python app_gold_price.py
```

## Response Codes

- `200 OK` - Success, all prices returned
- `503 Service Unavailable` - API error but using fallback rates
- `500 Internal Server Error` - Unexpected error

---

## Support & Questions

- **Price discrepancies?** Likely difference between global spot vs. local Oman rates
- **Need local rates?** Contact with Oman gold souk feed URLs
- **Purity questions?** See table above—24K is always the base
- **Integration help?** Check examples in this README or review:
  - `wan/gold_api.py` - Core API module
  - `app_gold_price.py` - Flask application with dashboard

---

**Built for real-time gold tracking with multi-purity support**
