# pubsub-webhook

Convert webhooks requests to PubSub messages.

This is a Cloud Function that takes an incoming HTTP POST payload and forwards it to a Pub/Sub topic. That's it. It's particularly useful if you want to serve a single webhook on Google Cloud and have it trigger multiple subscribers, whether it be Cloud Functions or App Engine applications (or anything else that can subscribe to a Pub/Sub topic).

![Diagram](pubsub-webhook.svg)
