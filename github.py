import requests
import re
import os


from event import Event

class GitHub:
    headers = {
        'Authorization': 'token {}'.format(os.environ['github_token'])
    }

    def __init__(self, payload):
        self.payload = payload

    def get_author(self):
        return self.payload['pull_request']['user']['login']

    def get_reviewer(self):
        return self.payload['pull_request']['requested_reviewers'][0]['login']

    def get_ticket_numbers(self):
        pull_request_number = self.payload['pull_request']['number']
        commit_url = self.payload['pull_request']['url'] + '/commits'
        r = requests.get(
            commit_url,
            headers=GitHub.headers
        )
        data = r.json()
        jira_tickets = set()

        for commit_data in data:
           commit_msg =  commit_data['commit']['message']
           jira_tickets_from_commit = re.findall(r'GJI-\d+', commit_msg)
           jira_tickets.update(jira_tickets_from_commit)
        return jira_tickets

    def get_fix_version(self):
        fix_version = None
        body = self.payload['pull_request']['body']
        pattern = '-fv (.*)'
        p = re.compile(pattern)
        result = p.search(body)
        if result:
            fix_version = result.group(1)
        return fix_version

    def get_action(self):
        if self.payload['action'] == 'review_requested':
            return Event.REVIEW_REQUEST
        elif self.payload['action'] == 'submitted' and self.payload['review']['state'] == 'changes_requested':
            return Event.CHANGE_REQUEST
        elif self.payload['action'] == 'closed':
            return Event.PR_MERGE
        return None

    def needs_qa(self):
        return self.payload['pull_request']['body'].find("QA") != -1
