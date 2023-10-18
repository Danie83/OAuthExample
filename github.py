import os
import requests
from dotenv import load_dotenv
from flask import Flask, redirect, request, render_template
from oauthlib.oauth2 import WebApplicationClient

# Load environment variables
load_dotenv()

app = Flask(__name__)
client_id = os.getenv('GITHUB_CLIENT_ID')
client_secret = os.getenv('GITHUB_CLIENT_SECRET')
redirect_uri = 'http://localhost:5000/callback'

# Initialize a web application flow using the client id from the configuration
oauth = WebApplicationClient(client_id)

@app.route('/')
def index():
    """Home page displayed when accessing the application."""

    return render_template('index.html')

@app.route('/login')
def login():
    """Prepares a complete url using the authorization url of the github platform
    and necessary credentials and then redirects the user to it.
    """
    
    authorization_url = oauth.prepare_request_uri(
        'https://github.com/login/oauth/authorize',
        redirect_uri=redirect_uri,
        scope=['user']
    )

    return redirect(authorization_url)

@app.route('/callback')
def callback():
    """After authorization, the user is redirected to /callback which is part of
    the complete url used when authorizing the user. This route is only available if the
    user has given authorization and is only accessible with the access token received.
    """

    token_url = 'https://github.com/login/oauth/access_token'
    token_params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': request.args.get('code'),
        'redirect_uri': redirect_uri
    }
    
    headers = { 'Accept': 'application/json' }
    response = requests.post(token_url, data=token_params, headers=headers)
    token = response.json().get('access_token')

    if token:
        user_info_url = 'https://api.github.com/user'
        headers = { 'Authorization': f'Bearer {token}' }

        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()
        
        return render_template('profile.html', user=user_info)

    return 'Login failed.'

if __name__ == '__main__':
    app.run(debug=True)