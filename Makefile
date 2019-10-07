SHELL := /bin/bash

rotate:
	@read -p "Provider [github or bitbucket]: " provider; \
	read -p "Username: " username; \
	read -s -p "Password: " password; \
	echo "{\"username\": \"$$username\", \"password\": \"$$password\"}" | \
		gcloud kms encrypt \
		--location global \
		--keyring=${BUILD_STATUS_KEYRING} \
		--key=${BUILD_STATUS_KEY} \
		--ciphertext-file=- \
		--plaintext-file=- | \
		gsutil cp - gs://${CREDENTIALS_BUCKET}/$$provider

decrypt:
	@read -p "Provider [github or bitbucket]: " provider; \
	gsutil cp gs://${CREDENTIALS_BUCKET}/$$provider - | \
		gcloud kms decrypt \
		--location global \
		--keyring=${BUILD_STATUS_KEYRING} \
		--key=${BUILD_STATUS_KEY} \
		--ciphertext-file=- \
		--plaintext-file=-

deploy:
	gcloud functions deploy \
		cloud-build-status \
		--source . \
		--runtime python37 \
		--entry-point build_status \
		--service-account cloud-build-status@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com \
		--set-env-vars KMS_CRYPTO_KEY_ID=${KMS_CRYPTO_KEY_ID},CREDENTIALS_BUCKET=${CREDENTIALS_BUCKET} \
		--trigger-topic=cloud-builds

unit:
	python -m pytest -W ignore::DeprecationWarning -v

integration: integration-github integration-bitbucket

integration-github:
	source tests/integration.sh && \
		run_github_test "WORKING" "pending" && \
		run_github_test "FAILURE" "error" && \
		run_github_test "SUCCESS" "success"

integration-bitbucket:
	source tests/integration.sh && \
		run_bitbucket_test "WORKING" "INPROGRESS" && \
		run_bitbucket_test "FAILURE" "FAILED" && \
		run_bitbucket_test "SUCCESS" "SUCCESSFUL"
