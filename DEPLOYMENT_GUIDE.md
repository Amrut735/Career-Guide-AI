# 🚀 Deployment Guide - CareerGuideAI to Google Cloud Platform

This guide will help you deploy your CareerGuideAI application to Google Cloud Platform so it's accessible to everyone on the internet.

## 📋 Prerequisites

1. **Google Cloud Account**: Sign up at [Google Cloud Console](https://console.cloud.google.com/)
2. **Google Cloud SDK**: Install the Google Cloud SDK
3. **Billing Enabled**: Enable billing on your Google Cloud project

## 🛠️ Installation Steps

### 1. Install Google Cloud SDK

**For Windows:**
```bash
# Download and install from: https://cloud.google.com/sdk/docs/install
# Or use PowerShell:
Invoke-WebRequest -Uri "https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe" -OutFile "GoogleCloudSDKInstaller.exe"
.\GoogleCloudSDKInstaller.exe
```

**For macOS/Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### 2. Initialize Google Cloud

```bash
# Login to your Google account
gcloud auth login

# Create a new project (or use existing)
gcloud projects create career-guide-ai-[YOUR-UNIQUE-ID]

# Set the project as default
gcloud config set project career-guide-ai-[YOUR-UNIQUE-ID]

# Enable required APIs
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Deploy to Google App Engine

```bash
# Deploy the application
gcloud app deploy

# Open the deployed application
gcloud app browse
```

## 🌐 Alternative Deployment Options

### Option 1: Heroku (Free Tier Available)
```bash
# Install Heroku CLI
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create career-guide-ai
git push heroku main
```

### Option 2: Railway (Free Tier Available)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

### Option 3: Render (Free Tier Available)
```bash
# Connect your GitHub repository
# Render will automatically deploy from your main branch
```

## 🔧 Configuration Files

### app.yaml (Google App Engine)
```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT app:app
instance_class: F1
automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

### Procfile (Heroku/Railway)
```
web: gunicorn app:app
```

## 💰 Cost Estimation

**Google App Engine (F1 instance):**
- Free tier: 28 instance hours/day
- Paid: ~$0.05/hour after free tier
- Estimated monthly cost: $0-15 (depending on usage)

**Other platforms:**
- Heroku: Free tier available, paid from $7/month
- Railway: Free tier available, paid from $5/month
- Render: Free tier available, paid from $7/month

## 🚀 Post-Deployment

1. **Test your application** at the provided URL
2. **Set up custom domain** (optional)
3. **Configure monitoring** and alerts
4. **Set up CI/CD** for automatic deployments

## 🔒 Security Considerations

1. **Environment variables**: Store sensitive data in environment variables
2. **HTTPS**: All platforms provide HTTPS by default
3. **Rate limiting**: Consider implementing rate limiting for production
4. **Backup**: Regular backups of your application data

## 📞 Support

- **Google Cloud**: [Documentation](https://cloud.google.com/docs)
- **Heroku**: [Documentation](https://devcenter.heroku.com/)
- **Railway**: [Documentation](https://docs.railway.app/)
- **Render**: [Documentation](https://render.com/docs)

---

**Your CareerGuideAI will be live and accessible to everyone on the internet! 🌍** 