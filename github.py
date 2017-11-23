import requests
import re
import os


from event import Event

def get_author(payload):
    return payload['pull_request']['user']['login']

def get_reviewer(payload):
    return payload['pull_request']['requested_reviewers'][0]['login']

def get_ticket_numbers(payload):
    pull_request_number = payload['pull_request']['number']
    commit_url = payload['pull_request']['url'] + '/commits'
    r = requests.get(
        commit_url,
        headers = {
            'Authorization': 'token {}'.format(os.environ['github_token'])
        }
    )
    data = r.json()
    jira_tickets = set()

    for commit_data in data:
       commit_msg =  commit_data['commit']['message']
       jira_tickets_from_commit = re.findall(r'GJI-\d+', commit_msg)
       jira_tickets.update(jira_tickets_from_commit)

    return jira_tickets

def get_action(payload):
    if payload['action'] == 'review_requested':
        return Event.REVIEW_REQUEST
    elif payload['action'] == 'submitted' and payload['review']['state'] == 'changes_requested':
        return Event.CHANGE_REQUEST
    elif payload['action'] == 'closed':
        return Event.PR_MERGE

    return None


def needs_qa(payload):
    if payload['pull_request']['body'].find("QA") != -1:
        return True
    return False
