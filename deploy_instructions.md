# How to Share Your Titanic Chatbot

## Quick Share (Same Network Only)
Send this link to people on the same WiFi/network:
**http://192.168.31.149:8501**

## Public Share (Anyone Can Access)
### Option 1: Streamlit Cloud (Easiest)
1. Push your code to GitHub
2. Go to https://share.streamlit.io/
3. Connect your GitHub repository
4. Select `frontend.py` as main file
5. Deploy - you'll get a public URL

### Option 2: Ngrok (Quick Public URL)
1. Install ngrok: `pip install pyngrok`
2. Run: `python -c "from pyngrok import ngrok; print(ngrok.connect(8501))"`
3. Share the generated ngrok URL

### Option 3: Railway/Render
1. Create accounts on Railway.app or Render.com
2. Connect your GitHub repo
3. Deploy as web service
4. Get public URL

## Required Files for Deployment
- `frontend.py` - Streamlit app
- `backend.py` - FastAPI server  
- `data_loader.py` - Data handling
- `requirements.txt` - Dependencies
- `titanic.csv` - Dataset (auto-downloaded)

## Note for Cloud Deployment
For cloud platforms, you'll need to modify the backend URL in `frontend.py` from `http://localhost:8000` to your deployed backend URL.
