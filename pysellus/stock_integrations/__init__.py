from pysellus.stock_integrations import terminal, slack

integration_classes = {
    'terminal': terminal.TerminalIntegration,
    'slack': slack.SlackIntegration
    # ...
}
