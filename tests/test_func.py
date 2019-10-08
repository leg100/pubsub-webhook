import flask
import pytest
from unittest import mock
from google.cloud import pubsub_v1

import main


@pytest.fixture
def env_vars(monkeypatch):
    monkeypatch.setenv('GCP_PROJECT', 'my-google-cloud-project')
    monkeypatch.setenv('TOPIC_NAME', 'my-topic')


@pytest.fixture
def req():
    req = mock.MagicMock(spec=flask.Request)
    req.method = 'POST'
    req.get_data = mock.MagicMock(return_value='{"foo": "bar"}')

    return req


@pytest.fixture
def client(mocker):
    mock_client = mock.MagicMock(pubsub_v1.publisher.client.Client)
    mocker.patch('main.pubsub.PublisherClient', return_value=mock_client)

    return mock_client


def test_wrong_method(req):
    req.method = 'GET'

    assert main.pubsub_webhook(req) == ('Method not allowed', 405)


def test_client(req, client, env_vars):
    assert main.pubsub_webhook(req) == 'OK'

    client.publish.assert_called_with(
            'projects/my-google-cloud-project/topics/my-topic',
            '{"foo": "bar"}')
