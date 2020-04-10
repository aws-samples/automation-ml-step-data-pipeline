import json
import os
import boto3
import logging

# Set Logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_cluster_id(event):
    if 'ClusterId' in event:
        return event['ClusterId']
        
def get_jar(program_name, program_mode):
    return 'command-runner.jar'

def get_args(event):
    program_mode = event['ProgramMode']
    program_name = event['ProgramName']
    program_file = event[program_name]
    ## Retrieving JobInput from input and adding as a input parameter to spark submit
    jobinput = event['JobInput']
    ## Retrieving ClusterSize from input and adding as a input parameter to spark submit
    clustersize = event['ClusterSize']
    ## ModelProgram S3 path is used to derive output S3 Path and assign to spark submit
    model_program = event['ModelProgram']
    modelprogram_output = model_program.rsplit('/', 2)[-3] +'/output'
    if program_name == 'PreProcessingProgram':
        modelprogram_output = model_program.rsplit('/', 2)[-3] +'/output/preprocessing'
        args = ['spark-submit','--deploy-mode','client','--master','yarn','--conf','spark.yarn.submit.waitAppCompletion=true','--conf','spark.yarn.appMasterEnv.PYSPARK_PYTHON=/mnt/anaconda3/bin/python3.7',program_file,jobinput,clustersize,program_mode,modelprogram_output]
    else:
        modelprogram_output = model_program.rsplit('/', 2)[-3] +'/output/model/'
        args = ['spark-submit','--deploy-mode','client','--master','yarn','--conf','spark.yarn.submit.waitAppCompletion=true','--conf','spark.yarn.appMasterEnv.PYSPARK_PYTHON=/mnt/anaconda3/bin/python3.7',program_file,jobinput,clustersize,modelprogram_output]    
    
    return args

def get_step_config(event):

    if 'ProgramName' in event:
        program_name = event['ProgramName']
    else:
        logger.info("ProgramName not found in event")
        raise Exception("No ProgramName parameter in input - should be PreProcessingProgram or ModelProgram")

    if 'ProgramMode' in event:
        program_mode = event['ProgramMode']
    else:
        logger.info("ProgramMode not found in input")
        raise Exception("No ProgramMode parameter in input")
    
    step_name = program_name
    step_jar = get_jar(program_name, program_mode)
    step_args = get_args(event)
    
    step_config = [
        {
            'Name' : step_name,
            'ActionOnFailure' : 'CONTINUE',
            'HadoopJarStep' : {
                'Jar' : step_jar,
                'Args' : step_args
            }
        }
        ]
    if 'main_class' in event:
        step_config[0]['MainClass'] = event['main_class']
    return step_config
    
def lambda_handler(event, context):
    logger.info('## EVENT')
    logger.info(event)
    
    #Get the id of the cluster and the config for the step. 
    client = boto3.client('emr')
    cluster_id = get_cluster_id(event)
    step_config = get_step_config(event)
    try:
      #Add a new emr step based on the inputs gathered above
      response = client.add_job_flow_steps(JobFlowId=cluster_id,Steps=step_config)
    except Exception as e:
      logger.info(f'Exception encountered: {e}')
      raise Exception("Failed to add emr step")
    return response
