from __future__ import print_function

import json
import logging

from github import GitHub
from jira import Jira

from event import Event
from column import Column

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    github = GitHub(event)
    fix_version = github.get_fix_version()
    ticket_numbers = github.get_ticket_numbers()
    assignee = get_assignee(github)

    for ticket in ticket_numbers:
        jira = Jira(ticket)
        jira.update_status(assignee=assignee, fix_version=fix_version)
        move_ticket(jira, github)

    return ""

def get_assignee(github):
    # TODO: Remove this when we have account mapping
    return None

    github_status = github.get_action()
    if github_status == Event.REVIEW_REQUEST:
        return github.get_reviewer()
    elif github_status == Event.CHANGE_REQUEST:
        return github.get_author()
    elif github_status == Event.PR_MERGE:
        return github.get_author()
    return None

def move_ticket(jira, github):
    current_state = jira.get_column()
    github_status = github.get_action()

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
        if (jira.get_ticket_type() == "Task") and not github.needs_qa():
            jira.move_to_column(Column.CLOSED)
        else:
            jira.move_to_column(Column.QA_REVIEW)

