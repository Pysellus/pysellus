import requests

from pysellus.interfaces import AbstractIntegration


class SlackIntegration(AbstractIntegration):
    def __init__(self, url, channel=None):
        self._url = url
        self._channel = channel
        self._payload = {}
        if self._channel:
            self._payload['channel'] = self._channel

    def on_next(self, element):
        self._compose_on_next_message(element)
        requests.post(self._url, json=self._payload)

    def on_error(self, element):
        self._compose_on_error_message(element)
        requests.post(self._url, json=self._payload)

    def on_completed(self):
        self._payload['text'] = 'All tests run, out of data.\nAll done for now...'
        requests.post(self._url, json=self._payload)

    def _compose_on_next_message(self, element):
        self._payload['attachments'] = [{
            'fallback': 'An error just error happened on {}'.format(element['test_name']),
            'pretext': 'An error just happened!',

            'title': 'Failed test',
            'title_link': 'http://example.org',

            'text': element['test_name'],
            'color': '#CF6160'
        }]

    def _compose_on_error_message(self, element):
        self._payload['attachments'] = [{
            'fallback': 'And just exception happened on {}'.format(element['test_name']),
            'pretext': 'An exception just happened!',

            'title': 'Wrongly-built test',
            'title_link': 'http://example.org',

            'text': element['test_name'],
            'color': 'danger'
        }]
