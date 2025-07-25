# Health Check Implementation for Flask Guestbook App

from flask import jsonify
from datetime import datetime
import psycopg
import os
from gbmodel.model_sql_postgres import DB_CONNECTION

def register_health_endpoints(app):
    """
    Register health check endpoints with the Flask app
    """
    
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
            # Test database connection
            conn = psycopg.connect(DB_CONNECTION)
            conn.close()
            
            return jsonify({
                "status": "ready",
                "database": "connected",
                "service": "guestbook",
                "timestamp": datetime.utcnow().isoformat()
            }), 200
            
        except psycopg.OperationalError as e:
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
