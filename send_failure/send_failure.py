import json
import os
import textwrap
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Config is not altered here because this Lambda works in push model, not pull one.
states_client = boto3.client('stepfunctions')


# noinspection PyUnusedLocal
def lambda_handler(event, context):

    logger.info('## EVENT')
    logger.info(event)
    
    if 'task_token' not in event:
        print("No task token, NOT signalling failure")
        return event
    task_token = event['task_token']
    try:
        error_info = event['stepstatus']['Status']['FailureDetails']
    except:
        error_info = {"Reason":"No FailureDetails in error"}
    error_message = ""
    if 'Message' in error_info:
        error_message = error_info['Message']
    elif 'Reason' in error_info:
        error_message = error_info['Reason']
    else:
        error_message = "Error"
    

    error_message = (error_message[:252] + '..') if len(error_message) > 252 else error_message

    try:
        states_client.send_task_failure(
            taskToken=task_token,
            error=textwrap.shorten(error_message, width=249),
            cause=textwrap.shorten(error_info.get('Reason', 'Cause is undefined.'), width=249)
        )
    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Sendign Failure Token Failed")
    return event
