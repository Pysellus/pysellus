import json

import requests

from pysellus.interfaces import AbstractIntegration


class TrelloIntegration(AbstractIntegration):
    def __init__(self, key, token, mode=None, trello_api_client=None, formatter=None, **kwargs):
        self.notification = self._get_notification_class_from_mode(mode)(**kwargs)

        self.trello_api_client = trello_api_client if trello_api_client is not None else TrelloAPI(
            key, token
        )

        self.formatter = formatter if formatter is not None else Formatter

    def _get_notification_class_from_mode(self, mode):
        return notifications.get(mode, ByCardNotification)

    def on_next(self, element):
        self._post_message(self.formatter.create_element_message(element))

    def _post_message(self, message):
        self.trello_api_client.post(
            self.notification.endpoint,
            self.notification.assemble_body(**message)
        )

    def on_error(self, element):
        self._post_message(self.formatter.create_error_message(element))

    def on_completed(self):
        self._post_message(
            self.formatter.create_completion_message('--------| All tests run |--------')
        )


class ByCardNotification:
    def __init__(self, card, checklist):
        self.card_id = card
        self.checklist_id = checklist

    @property
    def endpoint(self):
        return '/'.join(['cards', self.card_id, 'checklist', self.checklist_id, 'checkItem'])

    def assemble_body(self, title, content):
        return {
            'idChecklist': self.checklist_id,
            'name': title + ': ' + content
        }


class ByListNotification:
    def __init__(self, list):
        self.list_id = list

    @property
    def endpoint(self):
        return '/'.join(['lists', self.list_id, 'cards'])

    def assemble_body(self, title, content):
        return {
            'name': title,
            'desc': content
        }


notifications = {
    'card': ByCardNotification,
    'list': ByListNotification
}


class Formatter:
    @staticmethod
    def create_element_message(element):
        return {
            'title': element['test_name'],
            'content': markdown_quote(json.dumps(element['element']))
        }

    @staticmethod
    def create_error_message(element):
        return {
            'title': ' '.join([
                markdown_bold('ERROR'),
                'when running test:',
                element['test_name']
            ]),
            'content': '\n'.join([
                ':bangbang: When processing element',
                markdown_quote(json.dumps(element['element'])),
                'the following error was raised:',
                markdown_quote(repr(element['error']))
            ])
        }

    @staticmethod
    def create_completion_message(completion_phrase):
        return {
            'title': completion_phrase,
            'content': ''
        }


def markdown_quote(a_string):
    return enclose(a_string, '`')


def enclose(a_string, delimiter):
    return delimiter + a_string + delimiter


def markdown_bold(a_string):
    return enclose(a_string, '**')


class TrelloAPI:
    TRELLO_MAX_STRING_LENGTH = 16384
    BASE_URL = 'https://trello.com/1/'

    def __init__(self, key, token, http_client=requests):
        self._api_key = key
        self._api_token = token

        self._http_client = http_client

    def post(self, endpoint, body):
        self._http_client.post(
            url=TrelloAPI.BASE_URL + endpoint,
            params=self._query_parameters,
            json=self._cap_body(body)
        )

    @property
    def _query_parameters(self):
        return {
            'key': self._api_key,
            'token': self._api_token
        }

    def _cap_body(self, body):
        for key, value in body.items():
            if not isinstance(value, str):
                continue

            body[key] = value[:TrelloAPI.TRELLO_MAX_STRING_LENGTH]

        return body
