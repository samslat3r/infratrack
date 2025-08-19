from app import create_app
import os

app = create_app()

if __name__ == '__main__':
    # Don't run with debug=True in production
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)