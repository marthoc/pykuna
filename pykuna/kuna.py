import logging

from .camera import KunaCamera
from .errors import AuthenticationError, UnauthorizedError

API_URL = 'https://server.kunasystems.com/api/v1'
AUTH_ENDPOINT = 'account/auth'
CAMERAS_ENDPOINT = 'user/cameras'
RECORDINGS_ENDPOINT = 'recordings'

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
        self.cameras = {}
        self.recordings = {}

    def authenticate(self):
        """Login and get an auth token."""
        json = {
            'email': self._username,
            'password': self._password
        }

        result = self._request('post', AUTH_ENDPOINT, json=json)

        try:
            self._token = result['token']
        except TypeError:
            raise AuthenticationError('No Kuna API token response returned, check username and password.')
        except KeyError as err:
            _LOGGER.error('Error retrieving Kuna auth token: {}'.format(err))
            raise err

    def update(self):
        """Refresh the dict of all cameras in the Kuna account."""
        result = self._request('get', CAMERAS_ENDPOINT)

        for item in result['results']:
            self.cameras[item['serial_number']] = KunaCamera(item, self._request)

    def refresh_recordings(self):
        """Refresh the dict of all recordings in the Kuna account."""
        if not self.cameras:
            _LOGGER.warning('Cannot fetch recordings, no cameras in the Kuna account.')
            return

        for camera in self.cameras.values():
            params = {
                'serial_numbers[]': camera.serial_number
            }
            result = self._request('get', RECORDINGS_ENDPOINT, params=params)

            for recording in result['results']:
                self.recordings[recording['label']] = recording['mp4']

    def _request(self, method, path, json=None, params=None, thumbnail=False):
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
            result = req(url, headers=headers, json=json, params=params, timeout=3)
            result.raise_for_status()

            if thumbnail:
                return result.content

            return result.json()

        except HTTPError as err:
            if err.response.status_code == 401:
                raise UnauthorizedError('Kuna Auth Token invalid or stale?')
            else:
                _LOGGER.error('Kuna API request error: {}'.format(err))
        except Timeout:
            _LOGGER.error('Request to Kuna API timed out.')
            raise
