
import logging
import boto3
from botocore.exceptions import ClientError
import json
import decimal

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
#  ffmpeg -i Game.of.Thrones.S07E07.1080p.mkv -vcodec mpeg4 -b 4000k -acodec mp2 -ab 320k converted.avi


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class VideoConversion(object):
    def __init__(self, _config_):
        dynamodb = boto3.resource(_config_.get_database_name(), region_name=_config_.get_database_region())
        self.table = dynamodb.Table(_config_.get_database_table())
        logging.info(self.table.creation_date_time)

    def update_item_status(self, _id_, _status_):
        try:
            response = self.table.update_item(
                Key={'uuid': _id_},
                UpdateExpression='set video_status = :status',
                ExpressionAttributeValues={':status': _status_},
                ReturnValues="UPDATED_NEW"
            )
            logging.info(response)
        except ClientError as e:
            logging.error('Error when updating item: ', e)
        else:
            logging.info('Update item status succeeded: ')
            logging.info(json.dumps(response, indent=4, cls=DecimalEncoder))

