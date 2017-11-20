import requests
import re
from event import Event

def get_author(context):
    return context['pull_request']['user']['login']

def get_reviewer(context):
    return context[0]['requested_reviewers']['login']

def get_jira_code(context):
    pull_request_number = context['number']
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

def get_event(context):
    if context['action'] == 'review_requested':
        return Event.REVIEW_REQUEST
    elif context['action'] == 'submitted' and context['review']['state'] == 'changes_requested':
        return Event.CHANGE_REQUEST
    elif context['action'] == 'closed':
        return Event.PR_MERGE

    return None

