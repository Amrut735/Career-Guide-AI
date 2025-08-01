# Deployment Guide

This guide provides comprehensive instructions for deploying CareerGuideAI to various platforms and environments.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- pip (Python package manager)

### Local Development Setup
```bash
# Clone the repository
git clone https://github.com/Amrut735/Career-Guide-AI.git
cd Career-Guide-AI

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5001`

## 🌐 Production Deployment

### 1. Render (Recommended)

Render is a cloud platform that offers free hosting for web applications.

#### Setup Steps:
1. **Create Render Account**
   - Visit [render.com](https://render.com)
   - Sign up with your GitHub account

2. **Connect Repository**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the Career-Guide-AI repository

3. **Configure Service**
   ```
   Name: career-guide-ai
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Environment Variables** (Optional)
   ```
   FLASK_ENV=production
   PORT=10000
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your application
   - Your app will be available at `https://your-app-name.onrender.com`

#### Render Configuration Files

**`render.yaml`** (Optional):
```yaml
services:
  - type: web
    name: career-guide-ai
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: FLASK_ENV
        value: production
```

### 2. Heroku

Heroku is another popular platform for deploying Python applications.

#### Setup Steps:
1. **Install Heroku CLI**
   ```bash
   # Windows
   winget install --id=Heroku.HerokuCLI
   
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Linux
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

4. **Add Buildpacks**
   ```bash
   heroku buildpacks:set heroku/python
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open Application**
   ```bash
   heroku open
   ```

#### Heroku Configuration Files

**`Procfile`**:
```
web: gunicorn app:app
```

**`runtime.txt`**:
```
python-3.11.0
```

### 3. Railway

Railway is a modern deployment platform with excellent Python support.

#### Setup Steps:
1. **Visit Railway**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Deploy from GitHub**
   - Click "Deploy from GitHub repo"
   - Select your repository
   - Railway will auto-detect Python and deploy

3. **Configure Environment**
   - Set environment variables if needed
   - Railway will provide a public URL

### 4. DigitalOcean App Platform

DigitalOcean offers a managed platform for deploying applications.

#### Setup Steps:
1. **Create DigitalOcean Account**
   - Sign up at [digitalocean.com](https://digitalocean.com)

2. **Create App**
   - Go to Apps → Create App
   - Connect your GitHub repository

3. **Configure App**
   ```
   Source: GitHub
   Branch: main
   Build Command: pip install -r requirements.txt
   Run Command: gunicorn app:app
   ```

4. **Deploy**
   - Click "Create Resources"
   - Your app will be deployed automatically

### 5. AWS Elastic Beanstalk

For enterprise-grade deployments on AWS.

#### Setup Steps:
1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB Application**
   ```bash
   eb init -p python-3.11 career-guide-ai
   ```

3. **Create Environment**
   ```bash
   eb create production
   ```

4. **Deploy**
   ```bash
   eb deploy
   ```

#### AWS Configuration Files

**`.ebextensions/python.config`**:
```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: app:app
  aws:elasticbeanstalk:application:environment:
    FLASK_ENV: production
```

### 6. Google Cloud Platform (App Engine)

Google Cloud's managed platform for web applications.

#### Setup Steps:
1. **Install Google Cloud SDK**
   ```bash
   # Download from https://cloud.google.com/sdk/docs/install
   ```

2. **Initialize Project**
   ```bash
   gcloud init
   ```

3. **Deploy to App Engine**
   ```bash
   gcloud app deploy
   ```

#### GCP Configuration Files

**`app.yaml`**:
```yaml
runtime: python311
entrypoint: gunicorn -b :$PORT app:app

env_variables:
  FLASK_ENV: production
```

## 🔧 Environment Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_ENV` | Flask environment | `development` | No |
| `PORT` | Port number | `5001` | No |
| `SECRET_KEY` | Flask secret key | Auto-generated | No |
| `DEBUG` | Debug mode | `False` | No |

### Production Settings

For production deployments, ensure these settings:

```python
# In app.py
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
```

## 📦 Dependencies

### Required Packages
All dependencies are listed in `requirements.txt`:

```
Flask==2.3.3
gunicorn==21.2.0
reportlab==4.0.4
requests==2.31.0
```

### Adding New Dependencies
```bash
pip install new-package
pip freeze > requirements.txt
```

## 🔒 Security Considerations

### Production Security Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Use strong `SECRET_KEY`
- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Set up proper CORS headers
- [ ] Implement rate limiting
- [ ] Regular dependency updates
- [ ] Monitor application logs

### SSL/HTTPS
Most cloud platforms provide automatic SSL certificates:
- **Render**: Automatic HTTPS
- **Heroku**: Automatic SSL
- **Railway**: Automatic HTTPS
- **DigitalOcean**: Automatic SSL
- **AWS**: Configure in load balancer
- **GCP**: Automatic SSL

## 📊 Monitoring and Logs

### Application Logs
```bash
# Render
render logs

# Heroku
heroku logs --tail

# Railway
railway logs

# DigitalOcean
doctl apps logs your-app-id

# AWS
eb logs

# GCP
gcloud app logs tail
```

### Health Checks
Add a health check endpoint:

```python
@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
```

## 🔄 Continuous Deployment

### GitHub Actions
Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v1.0.0
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

### Automatic Deployments
Most platforms support automatic deployments:
- **Render**: Automatic on push to main
- **Heroku**: Automatic on push to main
- **Railway**: Automatic on push to main
- **DigitalOcean**: Automatic on push to main

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Issues
```bash
# Check if port is in use
netstat -an | grep :5001

# Use different port
export PORT=8000
python app.py
```

#### 2. Dependencies Issues
```bash
# Clear pip cache
pip cache purge

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

#### 3. Memory Issues
```bash
# Check memory usage
ps aux | grep python

# Optimize for low memory
export PYTHONOPTIMIZE=1
```

#### 4. Database Issues
- CareerGuideAI doesn't use a database
- All data is stored in session
- No database configuration needed

### Debug Mode
For debugging deployment issues:

```python
# Enable debug mode temporarily
app.config['DEBUG'] = True
```

## 📈 Performance Optimization

### Production Optimizations
1. **Use Gunicorn**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

2. **Enable Caching**
   ```python
   from flask_caching import Cache
   cache = Cache(app, config={'CACHE_TYPE': 'simple'})
   ```

3. **Compress Responses**
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

4. **Static File Optimization**
   - Minify CSS/JS
   - Enable gzip compression
   - Use CDN for static assets

## 🔄 Updates and Maintenance

### Updating Dependencies
```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade package-name

# Generate new requirements.txt
pip freeze > requirements.txt
```

### Application Updates
1. Make changes to your code
2. Test locally
3. Commit and push to GitHub
4. Platform will automatically redeploy

### Backup Strategy
- Code: GitHub repository
- Configuration: Environment variables
- Data: Session-based (no persistent data)

## 📞 Support

### Platform Support
- **Render**: [docs.render.com](https://docs.render.com)
- **Heroku**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **Railway**: [docs.railway.app](https://docs.railway.app)
- **DigitalOcean**: [docs.digitalocean.com](https://docs.digitalocean.com)
- **AWS**: [docs.aws.amazon.com](https://docs.aws.amazon.com)
- **GCP**: [cloud.google.com/docs](https://cloud.google.com/docs)

### Community Support
- GitHub Issues: [github.com/Amrut735/Career-Guide-AI/issues](https://github.com/Amrut735/Career-Guide-AI/issues)
- Documentation: [github.com/Amrut735/Career-Guide-AI](https://github.com/Amrut735/Career-Guide-AI)

---

**Last Updated**: August 1, 2025  
**Version**: 1.0 