from flask import Flask
from flask_cors import CORS
from api.v0_1.routes import api as api_v0_1

# from waitress import serve
print(__name__)
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_v0_1, url_prefix="/api/v0-1")


if __name__ == "__main__":
    app.run(debug=True)
    # serve(app, host='0.0.0.0', port=5070)
