import base64
import json
import flask
import pytest
from unittest import mock

import main


def event(func):
    def wrapper():
        data = func()
        encoded = base64.b64encode(json.dumps(data).encode())
        return {'data': encoded}

    return wrapper


@pytest.fixture
@event
def github_data():
    return {
        'sourceProvenance': {
            'resolvedRepoSource': {
                'commitSha': 'd985a61daddbcd9c05a06d199efc2aeca55e4a19',
                'repoName': 'github_leg100_webapp'
            }
        },
        'logUrl': 'https://console.cloud.google.com/gcr/builds/aeccd2ef-f51a-4a44-8e2e-0de2609ce367?project=292927648743',
        'buildTriggerId': '2bceb582-3141-44bf-b444-5640cbcaecc5',
        'status': 'SUCCESS'
    }


@pytest.fixture
@event
def bitbucket_data():
    return {
        'sourceProvenance': {
            'resolvedRepoSource': {
                'commitSha': '65ca6a99a2573f0f1ff5dc93f78a77966248ea2d',
                'repoName': 'bitbucket_garman_webapp'
            }
        },
        'logUrl': 'https://console.cloud.google.com/gcr/builds/aeccd2ef-f51a-4a44-8e2e-0de2609ce367?project=292927648743',
        'buildTriggerId': '2bceb582-3141-44bf-b444-5640cbcaecc5',
        'status': 'SUCCESS'
    }


@pytest.fixture
@event
def github_app_data():
    return {
        "sourceProvenance": {
            "resolvedStorageSource": {
                 "bucket": "292927648743.cloudbuild-source.googleusercontent.com",
                 "object": "ff7f18ef55982750630698ebffed9469a2d294db-9d56424f-c12b-4f7c-923b-34b9a77fcdaf.tar.gz",
                 "generation": "1570110452499581"
             }
        }
    }


@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv('GCP_PROJECT', 'my-google-cloud-project')
    monkeypatch.setenv('TOPIC_NAME', 'my-topic')


@pytest.fixture
def mock_client():
    class MockClient:
        def topic_path(self, project, topic):
            return f'projects/{project}/topics/{topic}'


        def get_topic(self, path):
            return path


        def publish(self, topic, data):
            return None


    return MockClient()


def test_wrong_method(env_vars):
    req = mock.MagicMock(spec=flask.Request)
    req.method = 'GET'

    assert main.pubsub_webhook(req) == ('Method not allowed', 405)


def test_func(mocker, env_vars):
    req = mock.MagicMock(spec=flask.Request)
    req.method = 'POST'

    import google
    mock_client = mock.MagicMock(google.cloud.pubsub_v1.publisher.client.Client)
    mocker.patch('main.pubsub.PublisherClient', return_value=mock_client)
    #class MockClient:
    #    def topic_path(self, project, topic):
    #        return f'projects/{project}/topics/{topic}'


    #    def get_topic(self, path):
    #        return path


    #    def publish(self, topic, data):
    #        return None

    assert main.pubsub_webhook(req) == 'OK'

    mock_client.topic_path.assert_called_with(
            'my-google-cloud-project',
            'my-topic')

