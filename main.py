from google.cloud import pubsub
import os


def whitelist_req(req, ranges):
    from ipaddress import ip_address, ip_network

    for r in ranges.split(','):
        if ip_address(req.remote_addr) in ip_network(r):
            return True

    return False


def pubsub_webhook(req):
    if req.method != 'POST':
        return ('Method not allowed', 405)

    if 'IP_WHITELIST' in os.environ:
        if not whitelist_req(req, os.environ['IP_WHITELIST']):
            return ('Forbidden', 403)

    client = pubsub.PublisherClient()

    topic_project = os.environ.get('TOPIC_PROJECT', os.environ['GCP_PROJECT'])
    topic_name = os.environ['TOPIC_NAME']

    topic = f'projects/{topic_project}/topics/{topic_name}'

    client.publish(topic, req.get_data())

    return 'OK'
