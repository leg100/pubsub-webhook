from google.cloud import pubsub
import os

def pubsub_webhook(req):

    if req.method != 'POST':
        return ('Method not allowed', 405)


    # TODO: whitelist requests (e.g. based on source IP)

    client = pubsub.PublisherClient()

    topic_project = os.environ.get('TOPIC_PROJECT', os.environ['GCP_PROJECT'])
    topic_name = os.environ['TOPIC_NAME']

    topic_path = client.topic_path(topic_project, topic_name)
    topic = client.get_topic(topic_path)
    client.publish(topic, req.data)

    return 'OK'
