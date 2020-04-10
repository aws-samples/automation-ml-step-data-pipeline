import os
import json
import boto3
import logging

# Set Logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_cluster_id(event):
    #check if there is a cluster id in the event input
    if 'ClusterId' in event:
        return event['ClusterId']
    else:
        print("No ClusterId parameter in input")
    
def lambda_handler(event, context):

    logger.info('## EVENT')
    logger.info(event)
  
    try:
        #Grab the status and state of the cluster from emr
        logger.info('Checking EMR Cluster Status')
        client = boto3.client('emr')
        cluster_id = get_cluster_id(event)
        response = client.describe_cluster(
            ClusterId=cluster_id
            )
        logger.info(response)
    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Could not find the status of the cluster")
    return { "State" : response['Cluster']['Status']['State']}
