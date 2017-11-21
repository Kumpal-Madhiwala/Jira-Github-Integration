from __future__ import print_function

import json
import logging
import github
from event import Event

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    event = github.get_action(event)
    if event == Event.REVIEW_REQUEST:
        logger.info('event is review request')
        logger.info('author: {}'.format(github.get_author(event)))
        logger.info('reviewer: {}'.format(github.get_reviewer(event)))
    elif: event == Event.CHANGE_REQUEST:
        logger.info('event is change request')
    elif: event == Event.PR_MERGE:
        logger.info('event is PR merge')

    return "hello world"
