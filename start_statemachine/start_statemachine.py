from __future__ import print_function
import boto3
import json
import os
import logging

# Set Logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

step_function_client = boto3.client('stepfunctions')
def lambda_handler(event, context):

    logger.info('## EVENT')
    logger.info(event)
    
    logger.info('Trying to Start State Machine')
    try:
        #Get the interesting variables from event and create local vars
        statemachine_arn = event['statemachine_arn']
        program_name = event['program_name']
        program_mode = event['program_mode']
        input_data = event['json_input']
        
        #Adjust the json with other values passed to this function
        input_data['ProgramName'] = program_name
        input_data['ProgramMode'] = program_mode

        json_data = json.dumps(input_data)

        print('State machine arn is: ' + statemachine_arn)
        print('Program name is: ' + program_name)
        print('Program mode is: ' + program_mode)
        print('Input for the state machine is: ' + json_data)

        #Start the step function based on these inputs
        response = step_function_client.start_execution(
            stateMachineArn=statemachine_arn,
            input=json_data
        )
        return('success')
    except Exception as e:
        logger.info(f'   Exception encountered: {e}')
        raise Exception("Could not start state machine")
