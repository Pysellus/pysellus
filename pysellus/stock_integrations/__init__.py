from pysellus.stock_integrations import terminal, slack, trello

integration_classes = {
    'terminal': terminal.TerminalIntegration,
    'slack': slack.SlackIntegration,
    'trello': trello.TrelloIntegration
}
