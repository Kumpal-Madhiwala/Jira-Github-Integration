

def get_author(context):
    return context['pull_request']['user']['login']

def get_reviewer(context):
    return context[0]['requested_reviewers']['login']
