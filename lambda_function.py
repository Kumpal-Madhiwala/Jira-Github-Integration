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

    ticket_numbers = github.get_ticket_numbers(event)

    for ticket in ticket_numbers:
        move_ticket(ticket, github_status)
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

def move_ticket(ticket, github_status):
    current_state = jira.get_column(ticket)

    if current_state == Column.TO_DO and github_status == Event.REVIEW_REQUEST:
        jira.start_ticket(ticket)
        jira.move_to_column(ticket, Column.CODE_REVIEW)
    elif current_state == Column.IN_PROGRESS and github_status == Event.REVIEW_REQUEST:
        jira.move_to_column(ticket, Column.CODE_REVIEW)
    elif current_state == Column.CODE_REVIEW and github_status == Event.CHANGE_REQUEST:
        jira.move_to_column(ticket, Column.IN_PROGRESS)
    elif current_state == Column.CODE_REVIEW and github_status == Event.PR_MERGE:
        jira.move_to_column(ticket, Column.QA_REVIEW)


