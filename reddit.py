
import os
from dotenv import load_dotenv
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, redirect, request, url_for, session
import requests

load_dotenv()

REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_REDIRECT_URI = "https://localhost:65010/callback"
REDDIT_API_BASE_URL = 'https://oauth.reddit.com'
REDDIT_API_ME_ENDPOINT = '/api/v1/me'

client = WebApplicationClient(REDDIT_CLIENT_ID)

app = Flask(__name__)

@app.route('/')
def home():
    from uuid import uuid4
    state = str(uuid4())
    authorization_url = client.prepare_request_uri(
        'https://www.reddit.com/api/v1/authorize',
        redirect_uri=REDDIT_REDIRECT_URI,
        state=state,
        scope=['identity'],
    )
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # code = request.args.get('code')
    token_url, headers, body = client.prepare_token_request(
        'https://www.reddit.com/api/v1/access_token',
        authorization_response=request.url,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET)
    )
    client.parse_request_body_response(token_response.text)
    session['token'] = client.token['access_token']
    return redirect(url_for('get_user_info'))

@app.route('/user_info')
def get_user_info():
    if 'token' in session:
        access_token = session['token']
        headers = {
            'Authorization': f'Bearer {access_token}',
            'User-Agent': 'YourAppName/1.0'
        }
        response = requests.get(f'{REDDIT_API_BASE_URL}{REDDIT_API_ME_ENDPOINT}', headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            return f'Authorized: {user_info["name"]}'
        else:
            return 'Failed to retrieve user information'
    else:
        return 'Access token not found. Please authorize access first.'

if __name__ == '__main__':
    app.run(debug=True, port=65010, ssl_context='adhoc')  
