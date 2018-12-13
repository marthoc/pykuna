import pykuna
import sys


def main():

    if len(sys.argv) < 3:
        print('Usage: python example.py USERNAME PASSWORD')
        exit(1)

    kuna = pykuna.KunaAPI(sys.argv[1], sys.argv[2])
    kuna.authenticate()
    kuna.update()

    for camera in kuna.cameras:
        print('-----------------------')
        print('{}: {}'.format(camera.name, camera.serial_number))
        print('-----------------------')
        for key in camera._raw:
            print(key)
        print('-----------------------')


main()
