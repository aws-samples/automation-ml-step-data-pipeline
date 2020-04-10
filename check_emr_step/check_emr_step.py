import os
import json
from datetime import date, datetime
import boto3
import logging

# Set Logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_cluster_id(event):
    if 'ClusterId' in event:
        return event['ClusterId']

def get_step_id(event):
    if 'step_id' in event:
        return event['step_id']
    else:
        return event['addstepstatus']['StepIds'][0]
def serialize_datetime(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
    
def lambda_handler(event, context):

    logger.info('## EVENT')
    logger.info(event)
    try:
        # Check the status of the EMR cluster
        logger.info('Getting the status of the EMR')
        client = boto3.client('emr')
        cluster_id = get_cluster_id(event)
        step_id = get_step_id(event)
        response = client.describe_step(
            ClusterId=cluster_id,
            StepId=step_id
            )
        datestring = serialize_datetime(response['Step']['Status']['Timeline']['CreationDateTime'])
        # TODO systematically serialize all datetimes
        response['Step']['Status']['Timeline'] = "REDACTED"
        logger.info(response)
    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Could not get the EMR Status")
    return response
