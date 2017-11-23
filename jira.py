import requests
import os

from column import Column

class Jira:
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic {}".format(os.environ['jira_token'])
    }

    def __init__(self, ticket):
        self.ticket = ticket
        self.payload = self.get_payload()

    # jira tickets have a transition from To Do to In Progress called 'Start'
    # which doesn't map to a column. If a ticket is in To Do and you want to move
    # it to In Progress, call this method
    def start_ticket(self):
        self.move_to_column("Start")

    def move_to_column(self, column):
        #some definition goes here
        transition_id = self.get_transition_id_from_column_name(column)
        payload = {
            "transition": {
                "id": str(transition_id)
            }
        }
        url = self.create_base_url("transitions")
        r = requests.post(
            url,
            json=payload,
            headers=Jira.headers
        )
        return r.status_code

    def update_status(self, **kwargs):
        # TODO: remove default assignee
        assignee = kwargs.pop('assignee', 'kumpal.madhiwala')
        fix_version = kwargs.pop('fix_version', None)

        self.set_assignee(assignee)
        if fix_version:
            self.add_fix_version(fix_version)

    def get_column(self):
        return Column.from_string(self.payload['fields']['status']['name'])

    def add_fix_version(self, fix_version):
        url = self.create_base_url()
        payload = {
            "update": {
                "fixVersions": [
                    {
                        "add": {
                            "name": fix_version
                        }
                    }
                ]
            }
        }
        r = requests.put(
            url,
            json=payload,
            headers=Jira.headers
        )
        return r.status_code

    def needs_product_review(self):
        labels = self.payload['fields']['labels']
        return "needs_product_review" in labels


    def get_ticket_type(self):
        return self.payload['fields']['issuetype']['name']

    # Private Methods

    def get_payload(self):
        url = self.create_base_url()
        response = requests.get(
            url,
            headers=Jira.headers
        )
        return response.json()

    def get_transition_id_from_column_name(self, column_name):
        url = self.create_base_url("transitions")
        response = requests.get(
            url,
            headers=Jira.headers
        )
        data = response.json()
        for transition in data["transitions"]:
            if transition["name"] == column_name:
                return transition["id"]

    def set_assignee(self, assignee):
        payload = {
            "name": assignee
        }
        url = self.create_base_url("assignee")
        response = requests.put(
            url,
            json=payload,
            headers=Jira.headers
        )
        return response.status_code

    def create_base_url(self, field=""):
        return "https://github-jira-integration.atlassian.net/rest/api/2/issue/{0}/{1}".format(self.ticket, field)

