from event import Event

def get_author(context):
    return context['pull_request']['user']['login']

def get_reviewer(context):
    return context[0]['requested_reviewers']['login']

def get_event(context):
    if context['action'] == 'review_requested':
        return Event.REVIEW_REQUEST
    elif context['action'] == 'submitted' and context['review']['state'] == 'changes_requested':
        return Event.CHANGE_REQUEST
    elif context['action'] == 'closed':
        return Event.PR_MERGE

    return None
