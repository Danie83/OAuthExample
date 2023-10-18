# OAuthExample
## Introduction
The code implements the OAuth 2.0 authorization code grant flow and facilitates the authorization through the Github OAuth service and retrieves user information from the Github API.
## Purpose
The purpose of this code is to demonstrate how to authorize resource access via Github OAuth using the WebApplicationClient from oauthlib python library. The application uses Flask to handle the authorization flow, redirecting the user to Github for authorization and then retrieving user information from Github's API.
## Code Overview
The code consists of several parts:
1. Importing necessary libraries and modules: os, requests, dotenv, WebApplicationClient, and Flask.
2. Configuration and environment variables: Loading environment variables using dotenv and setting up configuration constants for Github OAuth, including client ID, client secret.
3. Flask Application Setup:
* Creating a Flask application.
* Defining routes for the home page, login and callback.
4. Index Route (/) - index function:
* Constructs the Github authorization URL using the WebApplicationClient.
* Redirects the user to Github for authorization.
6. Login Route (/login) - login function:
- Creates and redirects the user to an url to authorize access to the user's github information.
7. Callback Route (/callback) - callback function:
* Handles the callback from Github after authorization.
* Retrieves the authorization code from the request.
* Exchanges the authorization code for an access token by making a request to Github's token URL using its client credentials.
* Uses the obtained access token to make authorized API requests on behalf of the user.
8. Main Execution:
* Runs the Flask application with debugging enabled on port 5000.

## Usage
To use this code for Github OAuth authorization:
* Create a Github OAuth application (requires a Github account).
* Set the required environment variables for Github client ID and client secret.
* Create an environment and install the required dependencies.
* Run the Python script.
* Access the application through a web browser.
* Navigate to the home page to initiate the authorization flow.

## Main Dependencies
* Python 3.11.2
* flask - Flask web framework
* dotenv - Loading environment variables from a .env file
* oauthlib - OAuth 2.0 client library
* requests - HTTP library for making requests

## Conclusion
This code demonstrates a basic implementation of Github OAuth authorization using Flask. It allows users to authorize the application to access their Github account and retrieve their authorized user information. Further improvements and customization can be made based on specific application requirements.