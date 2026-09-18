# Heroku Deployment Guide - Gold API for Oman

## ✅ Live Deployment in 5 Minutes

### Prerequisites (Download/Install)
- **Heroku CLI**: https://devcenter.heroku.com/articles/heroku-cli
- **Git**: Already installed (we use it)

---

## 🚀 Step-by-Step Deployment

### 1. Create Heroku Account (1 minute)
```bash
# Go to https://www.heroku.com/
# Sign up (free account)
# Confirm email
```

### 2. Login to Heroku
```bash
heroku login
# Browser opens - click "Log In"
# Returns to terminal: "Logged in as your@email.com"
```

### 3. Create Heroku App
```bash
# Navigate to the project directory
cd C:\Users\l\.copilot\repos\copilot-worktrees\Wan2.1\alshibli1998h-lgtm-stunning-goggles

# Create new Heroku app (replace with your app name)
heroku create gold-api-oman
```

Output:
```
Creating ⬢ gold-api-oman... done
https://gold-api-oman.herokuapp.com/ | https://git.heroku.com/gold-api-oman.git
```

**Your live URL:** `https://gold-api-oman.herokuapp.com/`

### 4. Set Environment Variables (IMPORTANT!)
```bash
# Set your GoldAPI.io API key (this is critical!)
heroku config:set GOLDAPI_KEY=your_api_key_here

# Verify it's set
heroku config
```

You should see:
```
GOLDAPI_KEY: your_api_key_here
```

### 5. Deploy to Heroku
```bash
# Push code to Heroku
git push heroku alshibli1998h-lgtm-add-gold-price-api:main

# Watch deployment logs
heroku logs --tail
```

Wait for:
```
remote: -----> Build succeeded!
remote: -----> Launching...
```

### 6. Test Your Live API
```bash
# Test the API
curl https://gold-api-oman.herokuapp.com/api/gold-price

# Or open in browser
https://gold-api-oman.herokuapp.com/
```

You should see gold prices in OMR! ✅

---

## 📋 Complete Deployment Checklist

- [ ] **Sign up** at https://www.heroku.com/
- [ ] **Install Heroku CLI** from https://devcenter.heroku.com/articles/heroku-cli
- [ ] **Run**: `heroku login`
- [ ] **Run**: `heroku create gold-api-oman` (or your app name)
- [ ] **Run**: `heroku config:set GOLDAPI_KEY=your_key_here`
- [ ] **Run**: `git push heroku alshibli1998h-lgtm-add-gold-price-api:main`
- [ ] **Wait** for deployment to complete
- [ ] **Test**: Open https://gold-api-oman.herokuapp.com/ in browser
- [ ] **See gold prices** in OMR on dashboard ✅

---

## 🔗 Your Live URLs

Once deployed:

| Service | URL |
|---------|-----|
| **Live Dashboard** | `https://gold-api-oman.herokuapp.com/` |
| **API Endpoint** | `https://gold-api-oman.herokuapp.com/api/gold-price` |
| **With Custom Premium** | `https://gold-api-oman.herokuapp.com/api/gold-price?premium=2.5` |

---

## 📊 Heroku App Management

### View Logs
```bash
heroku logs --tail
```

### Update API Key Later
```bash
heroku config:set GOLDAPI_KEY=new_key_here
```

### Update Code & Redeploy
```bash
# Make code changes
git add .
git commit -m "Update gold prices"

# Push to Heroku
git push heroku alshibli1998h-lgtm-add-gold-price-api:main
```

### View App Info
```bash
heroku info
```

### Stop/Delete App
```bash
heroku apps:destroy gold-api-oman
```

---

## ⚠️ Important Notes

1. **Free Heroku Tier Limits:**
   - App sleeps after 30 min inactivity
   - 550 free dyno hours/month (enough)
   - No cost for testing

2. **GoldAPI.io Free Tier:**
   - 100 calls/month (3 calls/day average)
   - Enough for most sites
   - Upgrade if you need more

3. **Custom Domain (Optional):**
   ```bash
   heroku domains:add yourdomain.com
   # Then update DNS at your domain registrar
   ```

---

## 🎉 Success!

Your gold API is now LIVE on Heroku! 

- Share the URL: `https://gold-api-oman.herokuapp.com/`
- Embed in your website
- Use the API endpoint in apps

**Next Steps:**
1. Integrate into your website using JavaScript from GOLD_API_QUICKSTART.md
2. Upgrade Heroku dyno if you get high traffic
3. Consider custom domain for professional look

---

## ❓ Troubleshooting

### "App not found" after deployment
```bash
# Check your app name
heroku apps

# Verify branch is correct
git push heroku alshibli1998h-lgtm-add-gold-price-api:main
```

### "Python not found" error
```bash
# Heroku uses runtime.txt to pick Python version
cat runtime.txt  # Should show python-3.11.6
```

### "GOLDAPI_KEY not set" error
```bash
# Set it
heroku config:set GOLDAPI_KEY=your_key_here

# Verify
heroku config
```

### Still having issues?
```bash
# View detailed logs
heroku logs --tail

# Check Heroku dashboard
# https://dashboard.heroku.com/apps/gold-api-oman
```

---

## 📞 Support

- Heroku Docs: https://devcenter.heroku.com/
- GoldAPI.io: https://www.goldapi.io/
- This Project: See GOLD_API_QUICKSTART.md

**Your app is now LIVE!** 🚀
