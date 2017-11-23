from __future__ import print_function

import json
import logging
import github
from jira import Jira

from event import Event
from column import Column

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    github_status = github.get_action(event)
    assignee = get_assignee(github_status, event)
    fix_version = github.get_fix_version(event)
    ticket_numbers = github.get_ticket_numbers(event)

    for ticket in ticket_numbers:
        jira = Jira(ticket)
        jira.update_status(assignee=assignee, fix_version=fix_version)
        move_ticket(jira, github_status, event)

    return ""

def get_assignee(github_status, context):
    # TODO: Remove this when we have account mapping
    return None

    if github_status == Event.REVIEW_REQUEST:
        return github.get_reviewer(context)
    elif github_status == Event.CHANGE_REQUEST:
        return github.get_author(context)
    elif github_status == Event.PR_MERGE:
        return github.get_author(context)

    return None

def move_ticket(jira, github_status, event):
    current_state = jira.get_column()

    if current_state == Column.TO_DO and github_status == Event.REVIEW_REQUEST:
        jira.start_ticket()
        jira.move_to_column(Column.CODE_REVIEW)
    elif current_state == Column.IN_PROGRESS and github_status == Event.REVIEW_REQUEST:
        jira.move_to_column(Column.CODE_REVIEW)
    elif current_state == Column.CODE_REVIEW and github_status == Event.CHANGE_REQUEST:
        jira.move_to_column(Column.IN_PROGRESS)
    elif current_state == Column.CODE_REVIEW and github_status == Event.PR_MERGE and jira.needs_product_review():
        jira.move_to_column(Column.PRODUCT_REVIEW)
    elif current_state == Column.CODE_REVIEW and github_status == Event.PR_MERGE:
        ticket_type = jira.get_ticket_type()
        go_to_qa = github.in_payload(event)
        move_to_dev_complete(go_to_qa, jira, ticket_type)


# checks GITHUB COMMIT description to determine QA_REVIEW or DONE
def move_to_dev_complete(go_to_qa, jira, ticket_type):
    if (ticket_type == "Task") and not go_to_qa:
        jira.move_to_column(Column.CLOSED)
    else:
        jira.move_to_column(Column.QA_REVIEW)
