import asyncio
import sys
from datetime import timedelta


async def main():

    if len(sys.argv) < 3:
        print('Usage: python example.py USERNAME PASSWORD')
        exit(1)

    # create an API object, passing username, password, and an instance of aiohttp.ClientSession
    from aiohttp import ClientSession
    from pykuna import KunaAPI
    
    websession = ClientSession()
    kuna = KunaAPI(sys.argv[1], sys.argv[2], websession)

    # authenticate() to get/refresh the access token
    await kuna.authenticate()

    # update() to populate kuna.cameras with a dict of cameras in the account;
    # key is camera serial number, value is camera object
    await kuna.update()

    for camera in kuna.cameras.values():
        # print the name and serial number of the camera
        print('Camera: {} (Serial No. {})'.format(camera.name, camera.serial_number))

        # retrieve a list of recording objects for all recordings for the past two hours
        recordings = await camera.get_recordings_by_time(timedelta(hours=2))
        for recording in recordings:
            print("Timestamp {}: {}".format(recording.timestamp, await recording.get_download_link()))

    await websession.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
