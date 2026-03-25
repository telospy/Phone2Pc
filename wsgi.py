# wsgi.py - For Gunicorn (Render, Railway)
from app import app

if __name__ == "__main__":
    app.run()