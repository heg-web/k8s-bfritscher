# Health Check Implementation for Flask Guestbook App
# Add these routes to your app.py file

from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

@app.route('/health')
def health_check():
    """
    Liveness probe endpoint - checks if the application is running
    Returns 200 if the app is alive, 500 if there are critical issues
    """
    try:
        # Basic application health check
        return jsonify({
            "status": "healthy",
            "service": "guestbook",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

@app.route('/ready')
def readiness_check():
    """
    Readiness probe endpoint - checks if the app is ready to serve traffic
    Returns 200 if ready, 503 if not ready (e.g., database not available)
    """
    try:
        # Check database connectivity
        db_host = os.getenv('DB_HOST', 'postgresql')
        db_port = os.getenv('DB_PORT', '5432')
        db_name = os.getenv('DB_NAME', 'guestbook')
        db_user = os.getenv('DB_USER', 'guestbook')
        db_pass = os.getenv('DB_PASS', 'guestbook')
        
        # Test database connection
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_pass
        )
        conn.close()
        
        return jsonify({
            "status": "ready",
            "database": "connected",
            "service": "guestbook",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except psycopg2.OperationalError as e:
        return jsonify({
            "status": "not_ready",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 503
    except Exception as e:
        return jsonify({
            "status": "not_ready",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 503

# Don't forget to import datetime at the top of your file:
# from datetime import datetime
