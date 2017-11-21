from __future__ import print_function

import json
import logging
import github
import jira

from event import Event
from column import Column

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # assignee = get_assignee(github_status, event)
    assignee="kumpal.madhiwala"
    github_status = github.get_action(event)
    column = get_move_to_column(github_status)

    ticket_numbers = github.get_ticket_numbers(event)

    for ticket in ticket_numbers:
        jira.move_to_column(ticket, column)
        jira.set_assignee(ticket, assignee)

    return ""

def get_assignee(github_status, context):
    if github_status == Event.REVIEW_REQUEST:
        return get_reviewer(context)
    elif github_status == Event.CHANGE_REQUEST:
        return get_author(context)
    elif github_status == Event.PR_MERGE:
        return get_author(context)

    return None

def get_move_to_column(github_status):
    if github_status == Event.REVIEW_REQUEST:
        return Column.CODE_REVIEW
    elif github_status == Event.CHANGE_REQUEST:
        return Column.IN_PROGRESS
    elif github_status == Event.PR_MERGE:
        return Column.QA_REVIEW

