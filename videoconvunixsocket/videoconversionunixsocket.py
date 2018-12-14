
import logging
import boto3
import ffmpy

from random import randint
from botocore.exceptions import ClientError

class VideoConversionUnixSocket(Thread) :
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)

    def __init__(self, _config_):
        self.s3 = boto3.resource('s3')
        self.client = boto3.client('s3')
        self.configuration = _config_

    def convert_video(self, _path_):
        key = self.get_last_split(_path_, '/')
        extension = self.get_last_split(key, '.')
        n = str(randint(0, 100))
        try:
            self.s3.Bucket(self.configuration.get_bucket_name()).download_file(key, 'local_temp_' + n + '.' + extension)
            ff = ffmpy.FFmpeg(
                executable='C:\\ffmpeg\\bin\\ffmpeg.exe',
                inputs={'local_temp_' + n + '.' + extension: None},
                outputs={'output_temp_' + n + '.avi': '-y -vcodec mpeg4 -b 4000k -acodec mp2 -ab 320k'}
            )
            ff.run()
            self.client.upload_file('output_temp_' + n + '.avi', self.configuration.get_bucket_name(),
                                    key.replace(extension, 'avi'))
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                logging.error('The object does not exist.')
            else:
                raise

    @staticmethod
    def get_last_split(_string_, _delimiter_):
        split = _string_.split(_delimiter_)
        return split[len(split) - 1]