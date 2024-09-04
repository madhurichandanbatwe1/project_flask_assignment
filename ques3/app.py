from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with your secret key

# Configure OAuth
oauth = OAuth(app)

# Google OAuth config
google = oauth.register(
    name='google',
    client_id='GOOGLE_CLIENT_ID',
    client_secret='GOOGLE_CLIENT_SECRET',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    authorize_kwargs=None,
    redirect_uri='http://localhost:5000/login/callback/google',
    client_kwargs={'scope': 'openid profile email'},
)

# Facebook OAuth config
facebook = oauth.register(
    name='facebook',
    client_id='FACEBOOK_APP_ID',
    client_secret='FACEBOOK_APP_SECRET',
    access_token_url='https://graph.facebook.com/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    authorize_params=None,
    authorize_kwargs=None,
    redirect_uri='http://localhost:5000/login/callback/facebook',
    client_kwargs={'scope': 'email'},
)


@app.route('/login/<provider>')
def login(provider):
    if provider == 'google':
        redirect_uri = url_for('callback', provider='google', _external=True)
        return google.authorize_redirect(redirect_uri)
    elif provider == 'facebook':
        redirect_uri = url_for('callback', provider='facebook', _external=True)
        return facebook.authorize_redirect(redirect_uri)

@app.route('/login/callback/<provider>')
def callback(provider):
    if provider == 'google':
        token = google.authorize_access_token()
        user_info = google.parse_id_token(token)
    elif provider == 'facebook':
        token = facebook.authorize_access_token()
        user_info = facebook.get('me?fields=id,name,email').json()

    # Store user information in session
    session['user'] = user_info
    return redirect('/profile')  # Redirect to a profile page or home page


@app.route('/profile')
def profile():
    user_info = session.get('user')
    if user_info:
        return f"Hello, {user_info['name']}!"
    return redirect(url_for('login', provider='google'))  # Redirect to login if not authenticated
