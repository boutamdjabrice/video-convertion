

import logging

from configuration.configuration import Configuration
from messaging.videoconversionmessaging import VideoConversionMessaging
from database.mongodb.videoconversion import VideoConversion
from videoconvunixsocket.conversion_service import VideoConversionUnixSocket


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
    configuration = Configuration()

    database = VideoConversion(configuration)
    conversion = VideoConversionUnixSocket(configuration)
    video_messaging = VideoConversionMessaging(configuration, database, conversion)

