import logging

from .camera import KunaCamera
from .errors import AuthenticationError, UnauthorizedError

API_URL = 'https://server.kunasystems.com/api/v1'
AUTH_ENDPOINT = 'account/auth'
CAMERAS_ENDPOINT = 'user/cameras'
USER_AGENT = 'Kuna/2.4.4 (iPhone; iOS 12.1; Scale/3.00)'
USER_AGENT_THUMBNAIL = 'Kuna/156 CFNetwork/975.0.3 Darwin/18.2.0'

_LOGGER = logging.getLogger(__name__)


class KunaAPI:
    """Class for interacting with the Kuna API."""

    def __init__(self, username, password):
        """Initialize the API object."""
        self._username = username
        self._password = password
        self._token = None
        self.cameras = []

    def authenticate(self):
        """Login and get an auth token."""
        json = {
            'email': self._username,
            'password': self._password
        }

        result = self._request('post', AUTH_ENDPOINT, json=json)

        if result is None:
            raise AuthenticationError('No token returned, check username and password')

        if 'token' in result:
            self._token = result['token']
            return

    def update(self):
        """Refresh the list of all cameras in the Kuna account."""

        result = self._request('get', CAMERAS_ENDPOINT)
        cameras = []

        for item in result['results']:
            cam = KunaCamera(item, self._request)
            cameras.append(cam)

        self.cameras = cameras

    def _request(self, method, path, json=None, thumbnail=False):
        """Make an API request"""
        import requests
        from requests.exceptions import HTTPError, Timeout

        url = '{}/{}/'.format(API_URL, path)
        headers = {
            'User-Agent': USER_AGENT
        }

        if method == 'post':
            req = requests.post
        elif method == 'patch':
            req = requests.patch
        else:
            req = requests.get

        if self._token:
            headers['Authorization'] = 'Token {}'.format(self._token)

        if thumbnail:
            headers['User-Agent'] = USER_AGENT_THUMBNAIL

        try:
            result = req(url, headers=headers, json=json, timeout=3)
            result.raise_for_status()

            if thumbnail:
                return result.content

            return result.json()

        except HTTPError as err:
            if err.response.status_code == 401:
                raise UnauthorizedError('Kuna Auth Token invalid or stale?')
        except Timeout:
            _LOGGER.error('Request to Kuna API timed out.')
