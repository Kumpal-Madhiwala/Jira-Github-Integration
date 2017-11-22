#Here are the wrapper methods for JIRA
import requests

from column import Column

headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic c2hlZXRoYWxhLnN3YW1pbmF0aGFuOkZyb290czE5NTk1"
}

# jira tickets have a transition from To Do to In Progress called 'Start'
# which doesn't map to a column. If a ticket is in To Do and you want to move
# it to In Progress, call this method
def start_ticket(ticket_number):
    move_to_column(ticket_number, "Start")

def move_to_column(ticket_number, column):
    #some definition goes here
    transition_id = get_transition_id_from_column_name(ticket_number, column)
    payload = {
        "transition": {
            "id": str(transition_id)
        }
    }

    url = create_base_url(ticket_number, "transitions")

    r = requests.post(
        url,
        json=payload,
        headers=headers
    )
    #Handle Errors here (If not found etc....)
    return r.status_code

def update_status(ticket_number, **kwargs):
    assignee = kwargs.pop('assignee', 'kumpal.madhiwala')
    fix_version = kwargs.pop('fix_version', None)

    set_assignee(ticket_number, assignee)
    if fix_version:
        add_fix_version(ticket_number, fix_version)

def set_assignee(ticket_number, assignee):
    payload = {
        "name": assignee
    }

    url = create_base_url(ticket_number, "assignee")

    response = requests.put(
        url,
        json=payload,
        headers=headers
    )
    return response.status_code

def get_transition_id_from_column_name(ticket_number, column_name):
    url = create_base_url(ticket_number, "transitions")
    response = requests.get(
        url,
        headers=headers
    )
    data = response.json()
    for transition in data["transitions"]:
        if transition["name"] == column_name:
            return transition["id"]

def get_column(ticket_number):
    url = create_base_url(ticket_number, '')

    response = requests.get(
        url,
        headers=headers
    )
    data = response.json()

    return Column.from_string(data['fields']['status']['name'])

def add_fix_version(ticket_number, fix_version):
    url = create_base_url(ticket_number, "")
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
        headers=headers
    )

    return r.status_code

def create_base_url(ticket_number, field):
    return "https://github-jira-integration.atlassian.net/rest/api/2/issue/{0}/{1}".format(ticket_number, field)
