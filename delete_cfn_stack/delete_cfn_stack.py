from __future__ import print_function
from _datetime import datetime
import json
import os
import boto3
import logging

# Set Logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

debug = True
demo_mode = False
legacy_demo_mode = False

sess = boto3.session.Session()
cfn = sess.client('cloudformation')
s3 = sess.client('s3')

def get_stack_name(stack_id):
    # initialize the return value
    response = dict()

    try:
        response = cfn.describe_stacks(
            StackName=stack_id
        )
        stack_name = response['Stacks'][0]['StackName']

    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Describing stack failed")

    return(stack_name)


def delete_stack(stack_id):

    try:
        # succesful stack delete returns None
        cfn.delete_stack(
            StackName=stack_id
        )

    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Deleting stack failed")

def lambda_handler(event, context):
  
    logger.info('## EVENT')
    logger.info(event)

    stack_id = event['stack_id']
    cfn_role = event['cfn_role']

    stack_name = get_stack_name(stack_id)
    logger.info('Deleting stack: ' + stack_name)
    logger.info('Stack id is: ' + stack_id)

    delete_stack(stack_id)
    logger.info('Stack deleted: ' + stack_name)
    
    return(stack_id)

