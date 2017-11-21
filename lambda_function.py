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
    github_status = github.get_action(event)
    ticket_number = 2
    #column = get_move_to_column(github_status)
    #assignee = get_assignee(github_status, event)
    column = "DEV"
    assignee="kumpal.madhiwala"

    jira.move_to_column(ticket_number, column)
    jira.set_assignee(ticket_number, assignee)

    return "hello world"

def get_assignee(enum, context):
    if enum == Event.REVIEW_REQUEST:
        return get_reviewer(context)
    elif enum == Event.CHANGE_REQUEST:
        return get_author(context)
    elif enum == Event.PR_MERGE:
        return get_author(context)

    return None

def get_move_to_column(enum):
    if enum == Event.REVIEW_REQUEST:
        return Column.CODE_REVIEW
    elif enum == Event.CHANGE_REQUEST:
        return Column.IN_PROGRESS
    elif num == Event.PR_MERGE:
        return Column.QA_REVIEW

def process_event(context):
    action = get_action(context)
    jira_code = get_jira_code(context)
    column_status = get_move_to_column(action)
    assignee = get_assignee(action, context)
    set_assignee(jira_code, assignee)
    move_to_column(jira_code, column_status)
