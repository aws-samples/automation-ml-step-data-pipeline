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
        print(f'Exception encountered: {e}')
        raise Exception("Describing stack failed")

    return(response)

def lambda_handler(event, context):

    logger.info('## EVENT')
    logger.info(event)

    stack_id = event['stack_id']
    logger.info("CloudFormation stack is:" + stack_id)

    response = describe_stack(stack_id)
    logger.info(response)

    cluster_id = response['Stacks'][0]['Outputs'][0]['OutputValue']
    logger.info('Cluster id is: ' + cluster_id)

    return(cluster_id)
