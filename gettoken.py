"""
This is a demo app for getting a token for a user in a trusted authentication scenario.
"""
from flask import Flask
from flask_cors import CORS

import logging
import requests

app = Flask(__name__)
CORS(app=app)

# constants for API usage.
TS_IP = "embed-1-do-not-delete.thoughtspotdev.cloud"
TS_USER = "tsadmin"
TS_PASSWORD = "Embedtest123%"
SECRET_KEY="e025d68e-4018-4fec-9120-e757c7b63d26"

LOGIN_API = "callosum/v1/tspublic/v1/session/login"

TOKEN_API = "callosum/v1/session/auth/token"
ACCESS_LEVEL = "FULL"

_log = logging.getLogger(__name__)


class GetAuthToken:
    """Manges getting an authentication token for a user."""

    def __init__(self):
        # TODO add parameters instead of constants.
        self.tsurl = TS_IP
        self.username = TS_USER
        self.password = TS_PASSWORD
        self.cookies = None

        self.session = requests.Session()
        self.disable_ssl = True
        if self.disable_ssl:
            self.session.verify = False
        self.session.headers = {"X-Requested-By": "ThoughtSpot"}

    def _get_login_url(self) -> str:
        """Returns a URL for logging in."""
        login_url = f"https://{self.tsurl}/{LOGIN_API}"
        _log.info(login_url)
        return login_url

    def _get_token_url(self) -> str:
        """Returns a url for getting the token for a given user."""
        token_url = f"https://{self.tsurl}/{TOKEN_API}"
        _log.info(token_url)
        return token_url

    def _login(self):
        """Logs in as the admin user for calling the APIs."""
        url = self._get_login_url()
        response = self.session.post(
            url, data={"username": self.username, "password": self.password}
        )

        if response.ok:
            self.cookies = response.cookies
            _log.info(f"Successfully logged in as {self.username}")
        else:
            _log.error(f"Failed to log in as {self.username}.  Status {response.status_code}")
            raise requests.ConnectionError(
                f"Error logging in to TS ({response.status_code})",
                response.text,
            )

    def is_authenticated(self) -> bool:
        """Returns true if the session is authenticated"""
        return self.cookies is not None

    def get_token(self, username: str) -> str:
        """
        Gets a token for the user with the username.
        """
        if not self.is_authenticated():
            try:
                self._login()
            except requests.exceptions.ConnectionError as ce:
                _log.error("Unable to log in.")
                return "Error accessing the ThoughtSpot cluster.  Check the cluster status and login details."

        url = self._get_token_url()
        data = {
            "secret_key": SECRET_KEY,
            "username": username,
            "access_level": "FULL"
        }

        response = self.session.post(url=url, data=data)

        if not response.ok:
            _log.error(f"Error getting token for {username}")
            error_msg = f"[{response.status_code}]: {response.text}"
            _log.error(error_msg)

            return error_msg

        return response.text


get_auth_token = GetAuthToken()


@app.route('/')
def index():
    return 'Use /gettoken/<username>'


@app.route("/gettoken/<username>", methods=["GET"])
def get_token(username: str) -> str:
    """Gets a token for the given user name."""
    return get_auth_token.get_token(username=username)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
