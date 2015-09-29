# Integrations

How do they work?

In STL, you decorate your test case functions with `failure`; in python, you do it with `@on_failure`, but internally, they work the same.

By now, you've seen the *terminal* integration. It is very simple — it just prints whatever error it happens to stdout.

**Pysellus** comes with three integrations by default: *terminal*, *slack* and *trello*, but you can make your own (See [defining custom integrations](.) - in progress).

---

#### Configuration

Most integrations will need some kind of parameters to work correctly, like API keys, or other.

Pysellus looks for this (and more) configuration data in a file, called `.ps_integrations.yml` by default, in the directory passed as an argument when starting the program.

This configuration file has a very simple structure:

```
notify:
    'user alias':
        integration_name:
            attr1: val1
            # ...
            attrn: valn
```
Here, we are defining an `integration_name` integration, with an alias of `user_alias`, and configuring it with n attributes and values.

#### Slack

The slack integration makes use of the [incoming webhooks api](https://api.slack.com/incoming-webhooks), and needs only a post url. To get one, you have to set up your own incoming webhook.

Additionally, you can pass a channel to your integration, and it will notify that channel.

To define an instance of a `slack` integration, with an alias of `foo`, we would write:

```
notify:
    'foo':
        slack:
            url: 'https://...' # slack post url
            # optionally, one of
            channel: '#some_channel'
            # or
            channel: '@some_user' 
```

Obviously, you can give it whatever name you want.

#### Trello

...

