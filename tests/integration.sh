#!/usr/bin/env bash

set -e
set -x

gcloud pubsub subscriptions delete webhook-integration-test || true
gcloud pubsub subscriptions create webhook-integration-test \
  --topic $TOPIC_NAME

gcloud functions call webhook --data '{"foo": "bar"}'

gcloud pubsub subscriptions pull webhook-integration-test \
  --format json | \
  jq '.[0].message.data' -r | \
    base64 -d | \
      jq -e '.foo == "bar"'
