from __future__ import print_function
import json
import logging
import os
import string
from _datetime import datetime
import boto3

# Set Logging level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

debug = True
demo_mode = False
legacy_demo_mode = False

cfn = boto3.client('cloudformation')
s3 = boto3.client('s3')

def get_parameters(p_url):
    # Grab the parameter values stored in S3 and convert them to a dictionary
    logger.info('Downloading parameter fies from S3')
    
    p_bucket = p_url.split('/')[3]
    p_key = p_url.rsplit('/', 1)[-1]

    # initialize the return value
    parm_dict =[]
    ## Added to support s3 bucket as a parameter
    s3_dict =[]
    try:
        s3.download_file(p_bucket, p_key, '/tmp/parms-local.json')
        parm_json = open('/tmp/parms-local.json').read()
        parm_dict = json.loads(parm_json)
        ## Added to support s3 bucket as a parameter
        s3_dict = {'ParameterKey':'BootstrapBucket','ParameterValue':p_bucket}
        parm_dict.append(s3_dict)
    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Downloading parameters failed")

    return(parm_dict)

def replace_cluster_name(parameter_dict, model_name):
    # Switch the ClusterName parameter to the ModelName provided to make it easier to identify
    new_parameter_dict = []
    model_name = sanitise_name(model_name)
    cluster_name = {"ParameterKey" : "ClusterName", "ParameterValue" : model_name}

    new_parameter_dict.append(cluster_name)
    for parameter in parameter_dict:
        if parameter['ParameterKey'] != 'ClusterName':
            new_parameter_dict.append(parameter)
    return new_parameter_dict

def sanitise_name(proposed_name):
    # Return an appropriate EMR cluster name from user-defined input (length, characters)
    # that is also used in CloudFormation stack name
    # No specific documentation was found for EMR naming, so we are following
    # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/Using_Tags.html   
    # CFN stack name must conform to [a-zA-Z][-a-zA-Z0-9]* further restricting naming

    valid_characters = string.ascii_letters + string.digits + '-'
    sanitised_name = ''.join(c for c in proposed_name if  c in valid_characters)
    if len(sanitised_name) > 128:
        # maximum length of CFN stack name is 128
        sanitised_name = sanitised_name[:128]
    if len(sanitised_name) < 4:
        # We have sanitised too much, so fall back
        sanitised_name = 'mlcluster'
    return sanitised_name

def launch_stack(stack_name, template_loc, cfn_role, parameters, tags):
    # initialize the return value
    logger.info('Launching the CFN Stack')
    response = dict()
    try:
        # Launch the cloudformation stack with the template URL and the parameters as a dict
        response = cfn.create_stack(
            StackName=stack_name,
            TemplateURL=template_loc,
            RoleARN=cfn_role,
            Parameters=parameters,
            Capabilities=['CAPABILITY_NAMED_IAM'],
            Tags=tags
        )
    except Exception as e:
        logger.info(f'Exception encountered: {e}')
        raise Exception("Creating stack failed")

    return response

def get_stack_name(prefix="auto-"):

    now = datetime.now()

    stack_name = prefix + now.strftime("%m%d%Y%H%M%S")
    stack_name = sanitise_name(stack_name)

    return(stack_name)

def lambda_handler(event, context):
    
    logger.info('## EVENT')
    logger.info(event)
    template_url = event['template_url']
    parameter_url = event['parameter_url']
    stack_prefix = event['stack_prefix']
    project_tag = event['project_tag']
    cfn_role = event['cfn_role']
    model_name = event['model_name']
    ## Added to support security group and subnet as a parameter
    security_grp = event['securitygroup']
    sbnet = event['subnet']
    ## Added to add dynamic core count for EMR cluster
    clustersize = event['clustersize']
    
    stack_prefix = model_name + "-" + stack_prefix
    stack_name = get_stack_name(stack_prefix)
    parameter_dict = get_parameters(parameter_url)
    parameter_dict = replace_cluster_name(parameter_dict, model_name)
    ## Added to support security group
    sg = {'ParameterKey':'AdditionalMasterSecurityGroup','ParameterValue':security_grp}
    parameter_dict.append(sg)
    ## Added to support subnet
    subnet = {'ParameterKey':'SubnetA','ParameterValue':sbnet}
    parameter_dict.append(subnet)
    ## Added to add dynamic core count for EMR cluster
    subnet = {'ParameterKey':'ClusterSize','ParameterValue':clustersize}
    parameter_dict.append(subnet)
    
    tag_dict = dict()
    tag_dict = [{ "Key": "Project", "Value": project_tag }]
    logger.info("Launching EMR stack with parameters:")
    #Launch the CFN Stack
    response = launch_stack(stack_name, template_url, cfn_role, parameter_dict, tag_dict)
    stack_id = response['StackId']
    logger.info('Stack id is: ' + stack_id)
    return(stack_id)

