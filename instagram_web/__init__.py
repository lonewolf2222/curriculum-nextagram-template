from app import app
from flask import render_template, request, redirect, url_for, session, abort, flash
from instagram_web.blueprints.users.views import users_blueprint
from instagram_web.blueprints.sessions.views import sessions_blueprint
from instagram_web.blueprints.images.views import images_blueprint
from instagram_web.blueprints.donations.views import donations_blueprint
from instagram_web.blueprints.follows.views import follows_blueprint
from flask_assets import Environment, Bundle
from .util.assets import bundles
from instagram_web.util.google_oauth import oauth
from instagram_web.util.facebook_oauth import facebook_oauth
from flask_session import Session
from models.form import ContactForm
from instagram_web.util.sendmail import send_email_contact
from werkzeug.contrib.fixers import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app)  # remove or comment this out if deploying to Heroku
oauth.init_app(app)
facebook_oauth.init_app(app)

Session(app)

assets = Environment(app)
assets.register(bundles)

app.register_blueprint(users_blueprint, url_prefix="/users")
app.register_blueprint(sessions_blueprint, url_prefix="/sessions")
app.register_blueprint(images_blueprint, url_prefix="/images")
app.register_blueprint(donations_blueprint, url_prefix="/donations")
app.register_blueprint(follows_blueprint, url_prefix="/follows")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(405)
def page_invalid(e):
    return render_template('405.html'), 405

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def page_forbidden(e):
    return render_template('403.html'), 403

@app.route("/")
def home(): 
    return redirect(url_for('users.index'))

@app.route("/contact", methods=['GET','POST'])
def contact():
    form=ContactForm(request.form)
    if not form.validate_on_submit():
        return render_template('contact.html', form=form)
    if request.method == 'POST':
        contents = request.form.get('contents')
        sender = request.form.get('email')
        send_email_contact(sender, contents)
        flash(u"Submitted",'info')
        return redirect(url_for('home'))


