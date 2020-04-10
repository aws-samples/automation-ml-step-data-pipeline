import json
import os
import logging
import time
import boto3
from botocore.config import Config

# Set Logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

step_function_client = boto3.client('stepfunctions', config=Config(read_timeout=65))

def lambda_handler(event, context):

    logger.info('## EVENT')
    logger.info(event)

    logger.info('Executing the Step Function')
    
    #get all the interesting variables from event and store them locally
    statemachine_arn= event['statemachine_arn']
    program_name = event['program_name']
    program_mode = event['program_mode']
    task_token = event['task_token']
    execution_name = event['execution_name']
    input_data = event['json_input']

    #update the json input with the details below
    input_data['ProgramName'] = program_name
    input_data['ProgramMode'] = program_mode
    input_data['task_token'] = task_token

    execution_name = execution_name + '-' + program_name + '-' + program_mode + str(time.time()).rsplit('.',1)[1]
    
    try:
      #Execute the state machine with the details above
      response = step_function_client.start_execution(
          stateMachineArn=statemachine_arn,
          name=execution_name,
          input=json.dumps(input_data)
      )
    except Exception as e:
      logger.info(f'Exception encountered: {e}')
      raise Exception("Could not execute the step function")

    logger.info(f'Nested execution arn is: {response["executionArn"]}')
    
    return('success')

