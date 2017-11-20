#Here are the wrapper methods for JIRA
import requests
import json
import pprint

headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic c2hlZXRoYWxhLnN3YW1pbmF0aGFuOkZyb290czE5NTk1"
}


def move_to_column(ticket_number, column):
    #some definition goes here
    transition_id = get_transition_id_from_column_name(ticket_number, column)
    print('The transition Id is')
    print(transition_id)
    payload = {
	   "transition": {
            "id": str(transition_id)
        }
    }

    r = requests.post(
        "https://tophat.atlassian.net/rest/api/2/issue/{0}/transitions".format(ticket_number),
        json=payload,
        headers=headers
    )
    #Handle Errors here (If not found etc....)
    return r.status_code

def set_asignee(ticket_number, asignee):
    payload = {
        "name": asignee
    }

    response = requests.put(
        "https://tophat.atlassian.net/rest/api/2/issue/{0}/assignee".format(ticket_number),
        json=payload,
        headers=headers
    )
    print(response.status_code)
    return response.status_code

def get_transition_id_from_column_name(ticket_number, column_name):
    response = requests.get(
        "https://tophat.atlassian.net/rest/api/2/issue/{0}/transitions".format(ticket_number),
        headers=headers
    )
    data = response.json()
    for transition in data["transitions"]:
        if transition["name"] == column_name:
            return transition["id"]




set_asignee('WEB-17331', 'sheethala.swaminathan')
