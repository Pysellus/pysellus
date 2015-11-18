from expects import expect, be, have_key

from pysellus.stock_integrations import slack, stock_integration_classes


with description('the slack integration module'):

    with it('should be in the integration classes dictionary'):
        expect(stock_integration_classes).to(have_key('slack'))
        expect(stock_integration_classes['slack']).to(be(slack.SlackIntegration))

    with it('should initialize with the correct arguments'):
        slack_url = 'an_url'
        slack_channel = 'a_channel'

        slack_instance = slack.SlackIntegration(slack_url)
        another_slack_instance = slack.SlackIntegration(slack_url, slack_channel)

        expect(slack_instance._url).to(be(slack_url))
        expect(slack_instance._channel).to(be(None))

        expect(another_slack_instance._url).to(be(slack_url))
        expect(another_slack_instance._channel).to(be(slack_channel))

    with it('should compose a correct on_next message'):
        slack_url = 'an_url'
        slack_element = {
            'test_name': 'some test'
        }

        expected_payload = {
            'attachments': [{
                'fallback': 'An error just error happened on {}'.format(slack_element['test_name']),
                'pretext': 'An error just happened!',

                'title': 'Failed test',
                'title_link': 'http://example.org',

                'text': slack_element['test_name'],
                'color': '#CF6160'
            }]
        }

        slack_instance = slack.SlackIntegration(slack_url)
        slack_instance._compose_on_next_message(slack_element)

        expect(slack_instance._payload).to(have_key('attachments'))

        pairs = zip(slack_instance._payload['attachments'], expected_payload['attachments'])

        # For some reason, comparing directly the dictionaries didn't work
        expect(any(x != y for x, y in pairs)).to(be(False))

    with it('should compose a correct on_error message'):
        slack_url = 'an_url'
        slack_element = {
            'test_name': 'some test'
        }

        expected_payload = {
            'attachments': [{
                'fallback': 'And just exception happened on {}'.format(slack_element['test_name']),
                'pretext': 'An exception just happened!',

                'title': 'Wrongly-built test',
                'title_link': 'http://example.org',

                'text': slack_element['test_name'],
                'color': 'danger'
            }]
        }

        slack_instance = slack.SlackIntegration(slack_url)
        slack_instance._compose_on_error_message(slack_element)

        expect(slack_instance._payload).to(have_key('attachments'))

        pairs = zip(slack_instance._payload['attachments'], expected_payload['attachments'])

        # For some reason, comparing directly the dictionaries didn't work
        expect(any(x != y for x, y in pairs)).to(be(False))
