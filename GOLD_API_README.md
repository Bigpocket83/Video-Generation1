# Gold Price API for Oman Market

This API provides live gold prices accurate to the Oman market, with prices converted to Omani Rial (OMR).

## Features

✅ **Live Gold Prices** - Real-time gold prices in USD per gram and ounce  
✅ **Oman Accurate** - Prices converted to OMR using live exchange rates  
✅ **Fallback Support** - Works even if primary API is unavailable  
✅ **Simple API** - Easy RESTful endpoint for your website  
✅ **Live Dashboard** - Beautiful web interface to display prices  

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

**Response:**
```json
{
  "currency": "OMR",
  "price_per_gram": 24.96,
  "price_per_ounce": 776.343,
  "timestamp": "2026-09-18T10:23:37.833032",
  "usd_to_omr_rate": 0.384,
  "source": "metals.live + exchangerate-api",
  "status": "success"
}
```

#### View Live Dashboard
Open your browser: `http://localhost:5000`

## Integration Examples

### JavaScript (Frontend)

```javascript
// Fetch gold prices
fetch('/api/gold-price')
  .then(res => res.json())
  .then(data => {
    console.log(`Gold: ${data.price_per_gram} OMR/gram`);
    console.log(`Gold: ${data.price_per_ounce} OMR/ounce`);
  });
```

### Python (Backend)

```python
from wan.gold_api import GoldPriceAPI

# Get current gold prices
prices = GoldPriceAPI.get_gold_price_oman()

print(f"Price per gram: {prices['price_per_gram']} OMR")
print(f"Price per ounce: {prices['price_per_ounce']} OMR")
```

### cURL

```bash
# Get prices
curl http://localhost:5000/api/gold-price

# Real-time endpoint (no caching)
curl http://localhost:5000/api/gold-price/live
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/gold-price` | GET | Get current gold price in OMR |
| `/api/gold-price/live` | GET | Real-time endpoint (no cache) |
| `/` | GET | View live dashboard |

## Data Sources

- **Gold Prices**: metals.live API (international spot price)
- **Exchange Rate**: exchangerate-api.com (USD → OMR conversion)
- **Fallback**: Approximate rates if APIs are unavailable

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

### Environment Variables

```bash
FLASK_ENV=production
FLASK_DEBUG=false
PORT=5000
```

## Testing

```bash
# Test the API module
python wan/gold_api.py

# Test the Flask app
python app_gold_price.py
```

## Response Codes

- `200 OK` - Success, prices returned
- `503 Service Unavailable` - API error but using fallback rates
- `500 Internal Server Error` - Unexpected error

## Accuracy Notes

- **Oman Rial**: Pegged to USD at 1 USD = 0.385 OMR (official rate)
- **Gold Price**: Updated daily, sourced from international spot markets
- **Ounce Conversion**: 1 troy ounce = 31.1035 grams

## Features for Your Website

1. **Display Current Price**: Show live gold prices updated every 5 minutes
2. **Price Alerts**: Get notified when prices change
3. **Historical Tracking**: Store prices for trend analysis
4. **Multi-Currency**: Already includes USD conversion

## Support

For issues or improvements, check:
- `wan/gold_api.py` - Core API module
- `app_gold_price.py` - Flask application with dashboard
- `requirements.txt` - Dependencies

---

**Built with ❤️ for the Oman Gold Market**
