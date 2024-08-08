import pytest
from threading import Event
from httmock import all_requests, urlmatch, HTTMock
from os import path
import sys
sys.path.append(path.dirname(path.realpath(__file__)) + "/../src")
from srsrpy import srsrpy  # noqa: E402


@pytest.fixture
def client():
    return srsrpy.ServiceRegistryClient('http://server_add',
                                        'my_name',
                                        'http://client_add')


@all_requests
def show_req(url, request):
    print(url.path)
    return {'status_code': 200,
            'content': '{"id":"foo"}'}


@urlmatch(path=r'/register$')
def register_mock(url, request):
    return {'status_code': 200,
            'content': '{"id":"123"}'}


@urlmatch(path=r'/deregister$')
def deregister_mock(url, request):
    return {'status_code': 200}


heart_event = Event()


@urlmatch(path=r'/heartbeat$')
def heartbeat_mock(url, request):
    heart_event.set()
    return {'status_code': 200}


def test_register(client):
    with HTTMock(register_mock):
        client.register()
    with HTTMock(deregister_mock):
        client.deregister()


def test_heartbeat(client):
    heart_event.clear()
    client.heartbeat_interval_seconds = 0.01
    with HTTMock(heartbeat_mock):
        with HTTMock(register_mock):
            client.register()

        heartbeat_sent = heart_event.wait(1)
        assert heartbeat_sent

        with HTTMock(deregister_mock):
            client.deregister()


def test_register_doesnt_throw_connectionerror(client):
    success = client.register()
    assert not success


def test_deregister_not_registered(client):
    client.deregister()


def test_deregister_doesnt_throw_connectionerror(client):
    with HTTMock(register_mock):
        client.register()

    client.deregister()


def test_heartbeat_doesnt_throw_connectionerror(client):
    client.heartbeat_interval_seconds = 0.01

    with HTTMock(register_mock):
        client.register()

    # Wait for a heartbeat, which should fail without throwing
    heart_event.clear()
    heart_event.wait(.05)

    with HTTMock(deregister_mock):
        client.deregister()
