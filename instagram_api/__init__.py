from app import app
from app import csrf
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app)

secret_key = os.environ.get("JWT_SECRET_KEY")
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app)

## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint
from instagram_api.blueprints.images.views import images_api_blueprint
from instagram_api.blueprints.sessions.views import sessions_api_blueprint

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(images_api_blueprint, url_prefix='/api/v1/images')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1')

csrf.exempt(sessions_api_blueprint)
csrf.exempt(users_api_blueprint)
csrf.exempt(images_api_blueprint)