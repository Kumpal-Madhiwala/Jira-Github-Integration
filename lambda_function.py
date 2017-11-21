from __future__ import print_function

import json
import logging
import github
import jira

from event import Event

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    github_status = github.get_action(event)
    ticket_number = github.get_ticket_number(event)
    #column = get_move_to_column(github_status)
    #assignee = get_assignee(github_status, event)
    column = "DEV"
    assignee="kumpal.madhiwala"

    jira.move_to_column(ticket_number, column)
    jira.set_assignee(ticket_number, assignee)

    return "hello world"
