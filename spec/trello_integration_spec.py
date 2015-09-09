import re
import json

from expects import expect, raise_error, match, be_a, equal, have_keys
from doublex import Spy, Mock, Stub, ANY_ARG
from doublex_expects import have_been_called, have_been_called_with, have_been_satisfied

from pysellus.stock_integrations import trello

with description('the Trello integration'):
    with description('requires the following arguments to be passed to the constructor:'):
        with it('API key'):
            def attempt_to_instantiate_without_api_key():
                trello.TrelloIntegration(token='a_token')

            expect(attempt_to_instantiate_without_api_key).to(
                raise_error(TypeError, match('missing.+key'))
            )

        with it('user token'):
            def attempt_to_instantiate_without_token():
                trello.TrelloIntegration(key='an_api_key')

            expect(attempt_to_instantiate_without_token).to(
                raise_error(TypeError, match('missing.+token'))
            )

    with description('offers two notification modes'):
        with description('by card'):
            with it("is selected by passing mode='card'"):
                integration = trello.TrelloIntegration(
                    key='an_api_key',
                    token='a_token',
                    mode='card',
                    card='some_card_id',
                    checklist='some_checklist_id'
                )

                expect(integration.notification).to(be_a(trello.ByCardNotification))

            with description('requires the following arguments to be passed to the constructor:'):
                with it('a card id'):
                    def attempt_to_instantiate_in_card_mode_without_card_id():
                        trello.TrelloIntegration(
                            key='an_api_key',
                            token='a_token',
                            mode='card',
                            checklist='some_checklist_id'
                        )

                    expect(attempt_to_instantiate_in_card_mode_without_card_id).to(
                        raise_error(TypeError, match('missing.+card'))
                    )

                with it('a checklist id'):
                    def attempt_to_instantiate_in_card_mode_without_checklist_id():
                        trello.TrelloIntegration(
                            key='an_api_key',
                            token='a_token',
                            mode='card',
                            card='some_card_id'
                        )

                    expect(attempt_to_instantiate_in_card_mode_without_checklist_id).to(
                        raise_error(TypeError, match('missing.+checklist'))
                    )

            with description('is implemented in the ByCardNotification class'):
                with before.each:
                    self.some_card_id = '1234'
                    self.some_checklist_id = '5678'

                    self.card_wise_notification = trello.ByCardNotification(
                        card=self.some_card_id,
                        checklist=self.some_checklist_id
                    )

                with it("has the right 'endpoint' attribute"):
                    # see https://trello.com/docs/api/card/index.html#post-1-cards-card-id-or-shortlink-checklist-idchecklist-checkitem
                    well_formed_endpoint = 'cards/' + self.some_card_id + '/checklist/' + self.some_checklist_id + '/checkItem'

                    expect(self.card_wise_notification.endpoint).to(equal(well_formed_endpoint))

                with it('has a method to create the body of the request'):
                    a_notification_message = {
                        'title': 'the title',
                        'content': 'the content'
                    }

                    assembled_body = self.card_wise_notification.assemble_body(**a_notification_message)

                    expect(assembled_body).to(have_keys('idChecklist', 'name'))

        with description('by list'):
            with it("is selected by passing mode='list'"):
                integration = trello.TrelloIntegration(
                    key='an_api_key',
                    token='a_token',
                    mode='list',
                    list='some_list_id'
                )

                expect(integration.notification).to(be_a(trello.ByListNotification))

            with description('requires more arguments to be passed to the constructor:'):
                with it('a list id'):
                    def attempt_to_instantiate_in_list_mode_without_list_id():
                        trello.TrelloIntegration(
                            key='an_api_key',
                            token='a_token',
                            mode='list'
                        )

                    expect(attempt_to_instantiate_in_list_mode_without_list_id).to(
                        raise_error(TypeError, match('missing.+list'))
                    )

            with description('is implemented in the ByListNotification class'):
                with before.each:
                    self.some_list_id = '1234'

                    self.list_wise_notification = trello.ByListNotification(
                        list=self.some_list_id
                    )

                with it("has the right 'endpoint' attribute"):
                    # see https://trello.com/docs/api/list/index.html#post-1-lists-idlist-cards
                    well_formed_endpoint = 'lists/' + self.some_list_id + '/cards'

                    expect(self.list_wise_notification.endpoint).to(equal(well_formed_endpoint))

                with it("has a method to create the body of the request"):
                    a_notification_message = {
                        'title': 'the title of the notification message',
                        'content': 'the content of the notification message'
                    }

                    assembled_body = self.list_wise_notification.assemble_body(**a_notification_message)

                    expect(assembled_body).to(have_keys('name', 'desc'))

    with it('defaults to card-wise notification'):
        integration = trello.TrelloIntegration(
            key='an_api_key',
            token='a_token',
            # mode='card',
            card='some_card_id',
            checklist='some_checklist_id'
        )

        expect(integration.notification).to(be_a(trello.ByCardNotification))

    with description("delegates to its trello_api_client's `post` method"):
        with before.each:
            self.notification_mock = Mock()
            self.trello_api_client_spy = Spy()
            self.integration = trello.TrelloIntegration(
                key='an_api_key',
                token='a_token',
                mode='card',
                card='some_card_id',
                checklist='some_checklist_id',
                trello_api_client=self.trello_api_client_spy
            )
            self.integration.notification = self.notification_mock

        with it('when `on_next` is called'):
            with self.notification_mock as notification_mock:
                notification_mock.endpoint
                notification_mock.assemble_body(ANY_ARG)

            some_element_to_notify_of = {
                'test_name': 'blah',
                'element': {}
            }

            self.integration.on_next(some_element_to_notify_of)

            expect(self.trello_api_client_spy.post).to(have_been_called.once)
            expect(self.notification_mock).to(have_been_satisfied)

        with it('when `on_error` is called'):
            with self.notification_mock as notification_mock:
                notification_mock.endpoint
                notification_mock.assemble_body(ANY_ARG)

            some_error_to_notify_of = {
                'test_name': 'blah',
                'element': {},
                'error': Exception('some error description')
            }

            self.integration.on_error(some_error_to_notify_of)

            expect(self.trello_api_client_spy.post).to(have_been_called.once)
            expect(self.notification_mock).to(have_been_satisfied)

    with description('delegates to its formatter for determining what is the title and what is the content of the notification'):
        with before.each:
            self.dummy_trello_api_client = Stub()
            self.formatter_spy = Spy()
            with self.formatter_spy as formatter_spy:
                formatter_spy.create_element_message(ANY_ARG).returns(dict())
                formatter_spy.create_error_message(ANY_ARG).returns(dict())
                formatter_spy.create_completion_message(ANY_ARG).returns(dict())

            self.integration = trello.TrelloIntegration(
                key='an_api_key',
                token='a_token',
                mode='card',
                card='some_card_id',
                checklist='some_checklist_id',
                trello_api_client=self.dummy_trello_api_client,
                formatter=self.formatter_spy
            )
            self.integration.notification = Stub()

        with it('calls Formatter.create_element_message when `on_next` is called'):
            some_element_to_notify_of = {
                'test_name': 'blah',
                'element': {}
            }

            self.integration.on_next(some_element_to_notify_of)
            expect(self.formatter_spy.create_element_message).to(have_been_called_with(some_element_to_notify_of).once)

        with it('calls Formatter#create_error_message when `on_error` is called'):
            some_element_error_to_notify_of = {
                'test_name': 'blah',
                'element': {},
                'error': Exception('the error description goes here')
            }

            self.integration.on_error(some_element_error_to_notify_of)
            expect(self.formatter_spy.create_error_message).to(have_been_called_with(some_element_error_to_notify_of).once)

        with it('calls Formatter#create_completion_message when `on_completed` is called'):
            self.integration.on_completed()
            expect(self.formatter_spy.create_completion_message).to(have_been_called_with(be_a(str)).once)

with description('the Formatter transforms notified elements into notification messages'):
    with context('Formatter#create_element_message'):
        with before.each:
            self.some_element_to_notify_of = {
                'test_name': 'some test',
                'element': {
                    'data': 1
                }
            }

            self.element_message = trello.Formatter.create_element_message(self.some_element_to_notify_of)

        with it('includes the test name in the title'):
            created_title = self.element_message['title']
            expect(created_title).to(match(self.some_element_to_notify_of['test_name']))

        with it('includes the element which was tested in the content'):
            created_content = self.element_message['content']
            expect(created_content).to(match(json.dumps(self.some_element_to_notify_of['element'])))

    with context('Formatter#create_error_message'):
        with before.each:
            self.some_element_to_notify_of = {
                'test_name': 'some test',
                'element': {
                    'data': 1
                },
                'error': Exception('the reason for the error')
            }

            self.error_message = trello.Formatter.create_error_message(self.some_element_to_notify_of)

        with it('includes an error notice in the title'):
            created_title = self.error_message['title']
            expect(created_title).to(match('error', re.IGNORECASE))

        with it('includes the test name in the title'):
            created_title = self.error_message['title']
            expect(created_title).to(match(self.some_element_to_notify_of['test_name']))

        with it('includes the element which was tested in the content'):
            created_content = self.error_message['content']
            expect(created_content).to(match(json.dumps(self.some_element_to_notify_of['element'])))

        with it('includes the type and message of the exception raised in the content'):
            created_content = self.error_message['content']
            expect(created_content).to(match(re.escape(repr(self.some_element_to_notify_of['error'])), re.DOTALL))

    with context('Formatter#create_completion_message'):
            with before.each:
                self.a_completion_message = '--- some completion message ---'
                self.created_completion_message = trello.Formatter.create_completion_message(self.a_completion_message)

            with it('includes a delimiter in the title'):
                created_title = self.created_completion_message['title']
                expect(created_title).to(match('---+'))

            with it('the content is the empty string'):
                created_content = self.created_completion_message['content']
                expect(created_content).to(equal(''))


with description('the Trello API object'):
    with description('requires the following arguments to be passed to the constructor:'):
        with it('API key'):
            def attempt_to_instantiate_without_api_key():
                trello.TrelloAPI(token='a_token')

            expect(attempt_to_instantiate_without_api_key).to(raise_error(TypeError, match('missing.+key')))

        with it('user token'):
            def attempt_to_instantiate_without_token():
                trello.TrelloAPI(key='an_api_key')

            expect(attempt_to_instantiate_without_token).to(raise_error(TypeError, match('missing.+token')))

    with description('abstracts POST actions on the Trello API:'):
        with before.each:
            self.some_api_key = 'abc'
            self.some_api_token = 'def'
            self.http_client_spy = Spy()

            self.trello_api = trello.TrelloAPI(
                key=self.some_api_key,
                token=self.some_api_token,
                http_client=self.http_client_spy
            )

            self.dummy_request_body = {}
            self.endpoint = 'path/to/some/endpoint'

        with it('calls the `post` mehtod of its http client with the proper url'):
            self.trello_api.post(self.endpoint, self.dummy_request_body)

            well_formed_url = 'https://trello.com/1/' + self.endpoint
            expect(self.http_client_spy.post).to(have_been_called_with(url=well_formed_url).once)

        with it('sends auth params passed in constructor as query parameters'):
            self.trello_api.post(self.endpoint, self.dummy_request_body)

            auth_params = {
                'key': self.some_api_key,
                'token': self.some_api_token
            }
            expect(self.http_client_spy.post).to(have_been_called_with(params=auth_params).once)

        with it('caps strings in payload to have a length of at most the limit imposed by Trello'):
            payload = {
                'a': 'a' * 50000,
                'b': 'b' * 200,
                'c': 42
            }

            capped_payload = {}
            for key, value in payload.items():
                if isinstance(value, str):
                    capped_payload[key] = value[:trello.TrelloAPI.TRELLO_MAX_STRING_LENGTH]
                else:
                    capped_payload[key] = value

            self.trello_api.post(self.endpoint, payload)

            expect(self.http_client_spy.post).to(have_been_called_with(json=capped_payload).once)
