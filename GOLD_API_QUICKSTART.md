# QUICK START: Gold API for Oman Prices

## ✅ Complete Setup (5 Minutes)

### 1. Get GoldAPI.io API Key (FREE)
```bash
# Go to https://www.goldapi.io/
# Click "Sign Up" (free tier)
# Go to Dashboard and copy your API key
# It looks like: f0d0xxxxxxxxxx
```

### 2. Set Environment Variable
```bash
export GOLDAPI_KEY=f0d0xxxxxxxxxx
```

### 3. Run the API Server
```bash
python app_gold_price.py
```

### 4. Access Live Prices
- **API Endpoint**: `http://localhost:5000/api/gold-price`
- **Live Dashboard**: `http://localhost:5000/`

---

## 🔧 Complete Configuration Reference

### Environment Variables (Set These)

```bash
# OPTION 1: Use GoldAPI.io (Best - Direct OMR)
export GOLDAPI_KEY=your_api_key_from_goldapi_io

# OPTION 2: Use Metals.Live with Oman Premium (No key needed)
export GOLD_PRICE_PREMIUM_MULTIPLIER=2.14
export GOLD_PRICE_FALLBACK_USD_OZ=2500.0

# OPTION 3: Update fallback price when gold prices change
export GOLD_PRICE_FALLBACK_USD_OZ=4400.0
```

---

## 📊 API Response Examples

### With GoldAPI.io (Direct OMR - Best):
```bash
curl http://localhost:5000/api/gold-price
```

Response:
```json
{
  "currency": "OMR",
  "price_type": "Oman Market",
  "purity_base": "24K (pure gold)",
  "per_gram": {
    "24K": 54.50,
    "22K": 49.96,
    "21K": 47.63,
    "18K": 40.88
  },
  "per_oz": {
    "24K": 1694.50,
    "22K": 1554.75,
    "21K": 1481.63,
    "18K": 1271.63
  },
  "source": "GoldAPI.io (Direct OMR)",
  "status": "success"
}
```

### With Metals.Live + Premium (USD Conversion):
```bash
curl 'http://localhost:5000/api/gold-price?premium=2.14'
```

Response includes premium_multiplier field.

---

## 🔌 Integration Code

### JavaScript
```javascript
// Fetch Oman gold prices
fetch('http://localhost:5000/api/gold-price')
  .then(res => res.json())
  .then(data => {
    console.log(`24K: ${data.per_gram['24K']} OMR/gram`);
    console.log(`22K: ${data.per_gram['22K']} OMR/gram`);
    console.log(`21K: ${data.per_gram['21K']} OMR/gram`);
  });
```

### Python
```python
from wan.gold_api import GoldPriceAPI

prices = GoldPriceAPI.get_gold_price_oman()
print(f"24K Gold: {prices['per_gram']['24K']} OMR/gram")
print(f"22K Gold: {prices['per_gram']['22K']} OMR/gram")
```

### cURL
```bash
# Get all prices
curl http://localhost:5000/api/gold-price

# With custom premium
curl 'http://localhost:5000/api/gold-price?premium=2.0'
```

---

## 🚀 Deployment

### Docker
```bash
docker build -t gold-api .
docker run -e GOLDAPI_KEY=your_key -p 5000:5000 gold-api
```

### Production (Gunicorn)
```bash
export GOLDAPI_KEY=your_key
gunicorn -w 4 -b 0.0.0.0:5000 app_gold_price:app
```

---

## 📋 API Provider Comparison

| Feature | GoldAPI.io | Metals.Live | Manual |
|---------|-----------|------------|--------|
| API Key Required | Yes (Free) | No | No |
| Direct OMR | ✅ Yes | ❌ No | ❌ No |
| Real-time | ✅ Yes | ✅ Yes | ❌ Static |
| Oman Accurate | ✅ Yes | ⚠️ With Premium | ⚠️ Depends |
| Free Tier | 100/month | Unlimited | - |
| Recommended | ✅ YES | Backup | Last Resort |

---

## ❓ FAQ

**Q: Which option should I use?**
A: **GoldAPI.io** - It has direct OMR support which is most accurate for Oman.

**Q: What if GoldAPI.io doesn't work?**
A: Falls back to Metals.Live with 2.14x premium multiplier automatically.

**Q: How often are prices updated?**
A: Real-time for both GoldAPI.io and Metals.Live (updates every few minutes).

**Q: Do I need to update anything manually?**
A: Only if you use the fallback - update `GOLD_PRICE_FALLBACK_USD_OZ` when gold prices change significantly.

**Q: What purity does it return?**
A: All purities (24K, 22K, 21K, 18K) derived from 24K base.

**Q: Can I use a different premium multiplier?**
A: Yes: `curl 'http://localhost:5000/api/gold-price?premium=2.5'`

---

## 🔑 Complete Configuration Checklist

- [ ] Sign up at https://www.goldapi.io/
- [ ] Copy API key to `export GOLDAPI_KEY=...`
- [ ] Run `python app_gold_price.py`
- [ ] Test: `curl http://localhost:5000/api/gold-price`
- [ ] Open browser: `http://localhost:5000/`
- [ ] Verify you see ~54 OMR/gram for 24K gold
- [ ] Integrate into your website using code examples above

---

## 📞 Support

- Check logs in `app_gold_price.py` output
- See `GOLD_API_SOLUTIONS.md` for detailed API info
- See `GOLD_API_README.md` for advanced configuration
- Python module: `wan/gold_api.py`

**Current Status**: ✅ Ready for production
