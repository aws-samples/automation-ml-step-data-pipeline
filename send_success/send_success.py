import json
import os
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
        print("No task token available, NOT signalling success")
        return event
    task_token = event['task_token']
    # `state` is a single-element array because it is an output
    # from Parallel state. Here we're unwrapping real result of
    # inner Execution.
    output_state = event
    try:
        states_client.send_task_success(
            taskToken=task_token,
            output=json.dumps(output_state),
        )
    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Sending Success Token Failed")
    return event
