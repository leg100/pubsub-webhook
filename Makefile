SHELL := /bin/bash

deploy:
	gcloud beta functions deploy \
		webhook \
		--source . \
		--runtime python37 \
		--entry-point pubsub_webhook \
		--service-account webhook@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com \
		--set-env-vars TOPIC_NAME=${TOPIC_NAME} \
		--trigger-http \
		--allow-unauthenticated

unit:
	python -m pytest -W ignore::DeprecationWarning -v

integration:
	./tests/integration.sh
