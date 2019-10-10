from abc import ABC, abstractmethod
import cv2
import time


# Camera resolution
RESOLUTION_WITH=1280
RESOLUTION_HEIGHT=720

# File camera
FOLDER = 'input'
FILE_NAME = 'camera'

pi_camera_available = True

try:
    import picamera
    import picamera.array
except ImportError:
    print('Warning: Pi camera is not available')
    pi_camera_available = False


class Camera(ABC):

    @abstractmethod
    def take_picture(self, iteration): pass

    @abstractmethod
    def initialize(self): pass


if pi_camera_available:

    class PiCamera(Camera):

        def __init__(self, resolution_width, resolution_height):
            self.resolution_width = resolution_width
            self.resolution_height = resolution_height
            self.camera = picamera.PiCamera()

        def initialize(self):
            self.camera.resolution = (self.resolution_width, self.resolution_height)
            time.sleep(3)

        def take_picture(self, _):
            picture = picamera.array.PiRGBArray(self.camera)
            self.camera.capture(picture, format="bgr")
            return picture.array

        def __enter__(self):
            return self.camera.__enter__()

        def __exit__(self):
            self.camera.__exit__()


class FileCamera(Camera):

    import os

    def __init__(self, folder, file_name):
        self.folder = folder
        self.file_name = file_name

    def initialize(self): pass

    def take_picture(self, iteration):
        path = '{}/{}-{}.png'.format(self.folder, self.file_name, iteration)
        result = cv2.imread(path)
        if result is None:
            raise FileNotFoundError('{} not found'.format(path))
        return result

    def __enter__(self): pass

    def __exit__(self): pass


class CameraFactory:
    @staticmethod
    def create(source, folder = FOLDER, file_name = FILE_NAME):
        if source is not None:
            if source == 'camera':
                try:
                    return PiCamera(RESOLUTION_WITH, RESOLUTION_HEIGHT)
                except NameError:
                    print('PiCamera not defined. May be missing -input argument.')
            elif source == 'file':
                try:
                    return FileCamera(folder, file_name)
                except NameError:
                    print('FileCamera not defined.')
        else:
            raise LookupError('No matching object found')
