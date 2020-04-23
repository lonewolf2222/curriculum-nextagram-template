from config import Config
from authlib.integrations.flask_client import OAuth

facebook_oauth = OAuth()

facebook_oauth.register('facebook',
    client_id=Config.FB_CLIENT_ID,
    client_secret=Config.FB_CLIENT_SECRET,
    access_token_url='https://graph.facebook.com/oauth/access_token',
    access_token_params=None,
    refresh_token_url=None,
    authorize_url='https://www.facebook.com/dialog/oauth',
    api_base_url='https://graph.facebook.com',
    client_kwargs={'scope': 'email'}
)