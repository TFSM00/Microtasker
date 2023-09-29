from main import app
from os import environ

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=5000,
            debug=environ.get('DEBUG') == '1',
            threaded=True)
