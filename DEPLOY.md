# 🚀 Deployment Guide - Fraud Shield

## Deploy to Render (Recommended)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/fraud-shield.git
   git push -u origin main
   ```

### Step 2: Deploy on Render

1. **Go to [Render.com](https://render.com)** and sign up/login

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository**
   - Select your repository
   - Click "Connect"

4. **Configure the service:**
   - **Name**: `fraud-shield` (or any name you like)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn flask_app:app`
   - **Plan**: Free (or upgrade for better performance)

5. **Add Environment Variables** (optional):
   - `FRAUD_SHIELD_SECRET`: Generate a random secret key
   - `PYTHON_VERSION`: `3.11.0`

6. **Click "Create Web Service"**

7. **Wait for deployment** (5-10 minutes first time)

8. **Your app will be live at**: `https://fraud-shield.onrender.com`

### Step 3: Verify Deployment

- Visit your app URL
- Test file upload functionality
- Check that model files are accessible

---

## Alternative: Deploy to Railway

### Step 1: Install Railway CLI
```bash
npm i -g @railway/cli
```

### Step 2: Deploy
```bash
railway login
railway init
railway up
```

---

## Alternative: Deploy to Heroku

### Step 1: Install Heroku CLI
Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

### Step 2: Deploy
```bash
heroku login
heroku create fraud-shield
git push heroku main
heroku open
```

---

## Troubleshooting

### Issue: "Model not found"
- **Solution**: Make sure `creditcard.pkl` is in your repository
- Add it to git: `git add creditcard.pkl`

### Issue: "Port error"
- **Solution**: Render automatically sets `$PORT` environment variable
- The Procfile already handles this

### Issue: "Build timeout"
- **Solution**: Free tier has build limits
- Consider upgrading or using a smaller model file

### Issue: "Memory limit"
- **Solution**: Free tier has 512MB RAM limit
- Upgrade to paid plan for more resources

---

## Environment Variables

Set these in Render dashboard → Environment:

- `FRAUD_SHIELD_SECRET`: Random secret key for Flask sessions
- `PYTHON_VERSION`: `3.11.0` (optional)

---

## Performance Tips

1. **Use smaller model files** if possible
2. **Enable caching** for static files
3. **Optimize image sizes** in templates
4. **Consider CDN** for static assets

---

## Need Help?

- Render Docs: https://render.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- Check logs in Render dashboard

