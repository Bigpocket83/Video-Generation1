# Gold Price API for Oman Market

This API provides live gold prices with purity-specific breakdowns (24K, 22K, 21K, 18K), converted to Omani Rial (OMR).

## ⚠️ Critical: Before Going Live

**This API returns GLOBAL SPOT prices**, not Oman-specific market rates:
- Current return: ~25 OMR/gram (global spot ~$2,050/oz)
- Your noted rate: ~54 OMR/gram (retail/local premium)

**Before deploying:**
1. Confirm which rate your site needs (spot vs. local retail/wholesale)
2. If you need Oman-specific rates, provide the feed URL or premium multiplier
3. We can add a configurable premium factor if needed

---

## Features

✅ **Multi-Purity Support** - Returns 24K, 22K, 21K, 18K prices  
✅ **Explicit Purity Base** - All prices derived from 24K pure gold  
✅ **Live Exchange Rates** - USD→OMR conversion using current rates  
✅ **Fallback Support** - Works even if primary API is unavailable  
✅ **RESTful API** - Easy JSON endpoint for your website  
✅ **Live Dashboard** - Beautiful interface to display prices  

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

**Response (with purity tiers):**
```json
{
  "currency": "OMR",
  "purity_base": "24K (pure gold)",
  "per_gram": {
    "24K": 25.29,
    "22K": 23.15,
    "21K": 22.08,
    "18K": 18.97
  },
  "per_oz": {
    "24K": 786.73,
    "22K": 719.48,
    "21K": 687.21,
    "18K": 590.19
  },
  "usd_to_omr_rate": 0.384,
  "timestamp": "2026-09-18T10:28:35.966886",
  "source": "metals.live",
  "status": "success"
}
```

#### View Live Dashboard
Open your browser: `http://localhost:5000`

---

## Gold Purity Reference

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
