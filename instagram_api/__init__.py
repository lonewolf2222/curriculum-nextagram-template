from app import app
from app import csrf
from flask_cors import CORS

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# CORS(app)

## API Routes ##
from instagram_api.blueprints.users.views import users_api_blueprint
from instagram_api.blueprints.images.views import images_api_blueprint
from instagram_api.blueprints.sessions.views import sessions_api_blueprint

app.register_blueprint(users_api_blueprint, url_prefix='/api/v1')
app.register_blueprint(images_api_blueprint, url_prefix='/api/v1')
app.register_blueprint(sessions_api_blueprint, url_prefix='/api/v1/')

csrf.exempt(sessions_api_blueprint)
csrf.exempt(users_api_blueprint)