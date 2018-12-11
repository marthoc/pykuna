# pykuna

## Python3 library for interacting with the Kuna camera mobile API

*Requirements:* python3, requests

Install pykuna with `python3 -m pip install pykuna`.

## Usage

pykuna's main class is KunaAPI. Create an API object, and authenticate it, like this:

```python
import pykuna

kuna = pykuna.KunaAPI(USERNAME, PASSWORD)
kuna.authenticate()
```

Where:

- `USERNAME` is the email address you use for the Kuna app; and,
- `PASSWORD` is your password for the Kuna app.

After authenticating, populate a list of all cameras in the Kuna account by calling the `update()` method on the API object:

```python
kuna.update()
```

## Methods

The following methods are available on a camera device object in the KunaAPI.cameras list:

- `update()` - refresh only that camera's properties from the API.
- `get_thumbnail()` - returns a camera snapshot as a jpeg image.
- `set_property(property=state)` - sets a property of the device. Properties currently settable via pykuna are:
  - `bulb_on` (boolean) - set the lightbulb  on (true) or off (false)
  - `led_mask` (boolean) - set the status led on the device on (true) or off (false)
  - `notifications_enabled` (boolean) - set notifications for the device on (true) or off (false)
  - `volume` (int) - set the speaker volume of the device (minimum 0, maximum 100)
- `light_on()` - turn on the camera's light bulb
- `light_off()` - turn off the camera's light bulb

## example.py

An example script is provided to demonstrate the usage of pykuna; it prints a list of cameras associated with the Kuna account, retrieves a snapshot from each camera, and toggles the camera's light bulb.

```python
python example.py USERNAME PASSWORD
```

## Caveats

pykuna interacts with Kuna's (private) mobile device API, which could change at any time. And, without official documentation or terms of service, there's no way to know what type or rate of usage may result in your account being banned by Kuna. Use carefully!

pykuna is synchronous.

pykuna was inspired by the investigative work of @loghound: https://github.com/loghound/kuna-camera-api, but does not yet implement all known endpoints; this project is primarily intended to interface Home Assistant with the Kuna API, and will be further developed with that goal in mind.

pykuna will hit v1.0.0 when it's ready for Home Assistant. Until then, pykuna's API may change at any time!

## Contributing

Please open issues or pull requests.
