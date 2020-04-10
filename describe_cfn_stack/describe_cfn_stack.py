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

cfn = boto3.client('cloudformation')
s3 = boto3.client('s3')

def describe_stack(stack_id):
    # initialize the return value
    response = dict()

    try:
        response = cfn.describe_stacks(
            StackName=stack_id
        )
    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Describing stack failed")

    return(response)

def lambda_handler(event, context):

    logger.info('## EVENT')
    logger.info(event)

    stack_id = event['stack_id']
    logger.info("CloudFormation stack is:" + stack_id)
    
    #Get the status of the cfn stack that we just built and pass it along as an output
    response = describe_stack(stack_id)
    status = response['Stacks'][0]['StackStatus']
    logger.info('Status is: ' + status)

    return(status)
