ENDPOINT_CAMERA = 'cameras'
ENDPOINT_USER = 'users'
ENDPOINT_THUMBNAIL = 'thumbnail'


class KunaCamera:
    """Represents a Kuna camera."""

    def __init__(self, raw, request):
        self._raw = raw
        self._request = request

    @property
    def url(self):
        return self._raw['url']

    @property
    def id(self):
        return self._raw['id']

    @property
    def serial_number(self):
        return self._raw['serial_number']

    @property
    def owner(self):
        return self._raw['owner']

    @property
    def name(self):
        return self._raw['name']

    @property
    def timezone(self):
        return self._raw['timezone']

    @property
    def status(self):
        return self._raw['status']

    @property
    def bulb_on(self):
        """
        Return the light status of the device.
        bool - true = on, false = off
        """
        return self._raw['bulb_on']

    @property
    def alarm_on(self):
        return self._raw['alarm_on']

    @property
    def led_mask(self):
        """Return the status led status of the device.
        bool - true = on, false = off
        """
        return self._raw['led_mask']

    @property
    def bluetooth_identifier(self):
        return self._raw['bluetooth_identifier']

    @property
    def updated_at(self):
        return self._raw['updated_at']

    @property
    def recordings_url(self):
        return self._raw['recordings_url']

    @property
    def users_url(self):
        return self._raw['users_url']

    @property
    def sensitivity(self):
        return self._raw['sensitivity']

    @property
    def build(self):
        """Return the firmware version of the device."""
        return self._raw['build']

    @property
    def volume(self):
        """
        Return the speaker volume level of the device.
        int - min 0, max 100
        """
        return self._raw['volume']

    @property
    def notifications_enabled(self):
        """
        Return the state of notifications of the device.
        boo - true = on, false = off
        """
        return self._raw['notifications_enabled']

    @property
    def location(self):
        return self._raw['location']

    @property
    def location_address(self):
        return self._raw['location_address']

    @property
    def subscription(self):
        return self._raw['subscription']

    @property
    def dawn_offset(self):
        return self._raw['dawn_offset']

    @property
    def dusk_offset(self):
        return self._raw['dusk_offset']

    @property
    def motion_timeout(self):
        return self._raw['motion_timeout']

    @property
    def mesh_group_id(self):
        return self._raw['mesh_group_id']

    @property
    def companions_count(self):
        return self._raw['companions_count']

    @property
    def down_at(self):
        return self._raw['down_at']

    @property
    def sight_option(self):
        return self._raw['sight_option']

    @property
    def sight_stationary_filter(self):
        return self._raw['sight_stationary_filter']

    @property
    def sight_stationary_mse_filter(self):
        return self._raw['sight_stationary_mse_filter']

    @property
    def play_msg_on_detect(self):
        return self._raw['play_msg_on_detect']

    @property
    def created_at(self):
        return self._raw['created_at']

    @property
    def sight_on_lite(self):
        return self._raw['sight_on_lite']

    @property
    def ip_address(self):
        return self._raw['ip_address']

    @property
    def recording_active(self):
        """Return the state of motion detection of the device.
        bool - true = detected, false = clear
        """
        return self._raw['recording_active']

    @property
    def brightness(self):
        return self._raw['brightness']

    @property
    def video_flip(self):
        return self._raw['video_flip']

    @property
    def sight_on(self):
        return self._raw['sight_on']

    @property
    def sight_on_override(self):
        return self._raw['sight_on_override']

    @property
    def autosight(self):
        return self._raw['autosight']

    @property
    def sight_permissions(self):
        return self._raw['sight_permissions']

    @property
    def server_up(self):
        return self._raw['server_up']

    @property
    def support_permission_end(self):
        return self._raw['support_permission_end']

    @property
    def custom_messages(self):
        return self._raw['custom_messages']

    def update(self):
        """Update device info from the Kuna cloud service."""
        result = self._request(
            'get',
            '{}/{}/'.format(ENDPOINT_CAMERA,
                            self.serial_number)
        )

        self._raw = result

    def get_thumbnail(self):
        """Retrieve a thumbnail image for the device."""
        result = self._request(
            'get',
            '{}/{}/{}/'.format(ENDPOINT_CAMERA,
                               self.serial_number,
                               ENDPOINT_THUMBNAIL),
            thumbnail=True
        )

        return result

    def set_property(self,
                     brightness: int = None,
                     bulb_on: bool = None,
                     led_mask: bool = None,
                     notifications_enabled: bool = None,
                     volume: int = None):
        """"Set a property of the device."""
        json = {
            key: value for key, value in {
                'brightness': brightness,
                'bulb_on': bulb_on,
                'led_mask': led_mask,
                'notifications_enabled': notifications_enabled,
                'volume': volume
            }.items() if value is not None
        }

        self._request(
            'patch',
            '{}/{}/'.format(ENDPOINT_CAMERA,
                            self.serial_number),
            json=json
        )

    def light_on(self):
        """Turn the light bulb on."""
        self.set_property(bulb_on=True)

    def light_off(self):
        """Turn the light bulb off."""
        self.set_property(bulb_on=False)
