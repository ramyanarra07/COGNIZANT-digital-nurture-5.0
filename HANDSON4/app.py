from flask import Flask, jsonify
from config import Config
from HO4app.routes import courses_bp

# 37. Define the application factory pattern
def create_app():
    app = Flask(__name__)
    
    # 38. Load configuration values
    app.config.from_object(Config)
    
    # 40. Register the Blueprint module
    app.register_blueprint(courses_bp)
    
    # 45. App-level API Error Handlers targeting clean JSON formats instead of HTML
    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify({
            'status': 'error',
            'data': {'message': 'The requested URL or resource was not found on this server.'}
        }), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            'status': 'error',
            'data': {'message': 'An internal server error occurred. Please try again later.'}
        }), 500
        
    return app

# Running file directly
if __name__ == '__main__':
    application = create_app()
    application.run()