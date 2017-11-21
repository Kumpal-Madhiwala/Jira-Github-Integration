import requests
import re
from event import Event

def get_author(payload):
    print payload
    return payload['pull_request']['user']['login']

def get_reviewer(payload):
    return payload['pull_request']['requested_reviewers'][0]['login']

def get_ticket_number(payload):
    pull_request_number = payload['pull_request']['number']
    url = 'https://api.github.com/repos/tophatmonocle/thm-mobile-android/pulls/{}/commits'.format(pull_request_number)
    r = requests.get(url)
    data = r.json()
    commit_msg = []
    jira_ticket = None

    for commit_data in data:
       commit_msg =  commit_data['commit']['message']
       jira_ticket = re.match(r'AN-\d+', commit_msg)
       if jira_ticket:
           jira_ticket = jira_ticket.group(0)
           break

    return jira_ticket

def get_action(payload):
    if payload['action'] == 'review_requested':
        return Event.REVIEW_REQUEST
    elif payload['action'] == 'submitted' and payload['review']['state'] == 'changes_requested':
        return Event.CHANGE_REQUEST
    elif payload['action'] == 'closed':
        return Event.PR_MERGE

    return None
