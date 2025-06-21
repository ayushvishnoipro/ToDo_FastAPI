# Deploying Task Manager to Render

This guide will walk you through deploying your FastAPI Task Manager application on Render.

## Prerequisites

- A GitHub account
- Your project pushed to a GitHub repository
- A free Render account (sign up at https://render.com)

## Deployment Steps

### Step 1: Push your code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add your files
git add .

# Commit your changes
git commit -m "Initial commit"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/task-manager.git

# Push your code to GitHub
git push -u origin main
```

### Step 2: Deploy the Backend on Render

1. Log in to your Render account
2. Click on "New" and select "Web Service"
3. Connect your GitHub repository
4. Configure the following settings:
   - **Name**: task-manager-api
   - **Environment**: Python
   - **Region**: Choose the closest region to your users
   - **Branch**: main (or your preferred branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

5. Click "Create Web Service"

### Step 3: Update the Backend Secret Key

1. In the Render dashboard, go to your task-manager-api service
2. Click on "Environment" in the left sidebar
3. Add the following environment variable:
   - **Key**: SECRET_KEY
   - **Value**: (generate a secure random string)
4. Click "Save Changes"

### Step 4: Deploy the Frontend on Streamlit Cloud

1. Create a separate GitHub repository for your frontend code
2. Push only the frontend folder to this repository
3. Log in to Streamlit Cloud (https://share.streamlit.io/)
4. Deploy a new app and connect it to your frontend repository
5. Set the main file path to: `app.py`

### Step 5: Update the API URL in the Frontend

1. In your Streamlit Cloud deployment settings, add an environment variable:
   - **Key**: API_URL
   - **Value**: Your Render backend URL (e.g., https://task-manager-api.onrender.com)

## Testing the Deployment

After deployment:

1. Wait for both services to finish deploying
2. Open your Streamlit Cloud URL
3. Try to sign up, log in, and create tasks
4. Verify that everything works as expected

## Troubleshooting

- **Database Issues**: If you're using SQLite, make sure the database file is in a writable directory.
- **CORS Errors**: Check that your FastAPI backend allows requests from your Streamlit frontend domain.
- **Authentication Issues**: Make sure the JWT secret key is properly set in the environment variables.

## Upgrading to PostgreSQL (Optional)

For production use, you may want to switch from SQLite to PostgreSQL:

1. Create a PostgreSQL database on Render
2. Update the database connection string in your backend code
3. Add the database connection string as an environment variable in your backend service

```python
# Update database.py with:
import os
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./tasks.db")
```