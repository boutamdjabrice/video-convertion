
import time
import logging
import json

from google.cloud import pubsub_v1

logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)

# rabbitmqadmin -H localhost -u ezip -p pize -V ezip purge queue name=video-conversion-queue
# rabbitmqadmin -H localhost -u ezip -p pize -V ezip get queue=video-conversion-queue

class VideoConversionMessaging(Object):
    def __init__(self, _config_, database_service, conversion_service):
        project_id = _config_.get_google_project_id()
        subscription_name = _config_.get_google_subscription_name()

        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(project_id, subscription_name)

        def callback(message):
            logging.info('Received message: {}'.format(message.data))
            received_data = json.loads(message.data.decode('utf-8'))
            conversion_service.convert_video(received_data['originPath'])
            database_service.update_item_status(received_data['uuid'], 'converted')
            message.ack()

        subscriber.subscribe(subscription_path, callback=callback)

        logging.info('Listening for messages on {}'.format(subscription_path))
        while True:
            time.sleep(60)
