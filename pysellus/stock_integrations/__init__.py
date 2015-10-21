from pysellus.stock_integrations import terminal, slack, trello

stock_integration_classes = {
    'terminal': terminal.TerminalIntegration,
    'slack': slack.SlackIntegration,
    'trello': trello.TrelloIntegration
}
