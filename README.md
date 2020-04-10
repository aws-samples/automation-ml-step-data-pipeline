# Automation of ML using Step Functions

Below are the steps listed to execute the code once it is downloaded.

## Prerequisite

* Python 3
* Created an AWS account.
* Configured IAM permissions.
* Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
* Installed Docker. Note: Docker is only a prerequisite for testing your application locally.
* Installed Homebrew. Note: Homebrew is only a prerequisite for Linux and macOS. 
* Install [AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).Note: Make sure you have version 0.33.0 or later. You can check which version you have by executing the command sam --version

## Step 1 Download Applciation

* Download the application from github repo (**Need to update the path Or install using [SAR](SAR path)**)

## Step 2 Initiate Application

* Go to the path and initiate application. For more details please click on this [link](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-init.html).
  
   **Command to run:**
   ~~~~ aws
   sam init -l /Users/sam-demo/step-pipeline.zip
   ~~~~

## Step 3 Create S3 Bucket and move dependencies

* S3 bucket creation.
  
  **Command to run:**
  
  ~~~~ aws
  aws s3 mb s3://blog-step-pipeline-demo
  ~~~~

* Move data to the bucket created.
  **Command to run:**
  
  ~~~~ aws
  aws s3 cp sample_ml_code/kmeansandey.py s3://<your bucket name>/testcode/kmeansandey.py
  aws s3 cp sample_ml_code/kmeanswsssey.py s3://<your bucket name>/testcode/kmeanswsssey.py
  aws s3 cp emr/bootstrapactions.sh s3://<your bucket name>/emr-bootstrap-scripts/bootstrapactions.sh
  aws s3 cp cemr/emr-cluster-config.json s3://<your bucket name>/emr-cluster-config.json
  aws s3 cp emr/emr-cluster-sample.yaml s3://<your bucket name>/emr-cluster-sample.yaml
  ~~~~

## Step 4 Update samconfig.toml

* Update bucket name, prefix, region, stackname and parameter_overrides path/**samconfig.toml**

    ~~~~aws
    version = 0.1
    [default]
    [default.deploy]
    [default.deploy.parameters]
    stack_name = "step-pipeline"
    s3_bucket = "blog-step-pipeline-demo"
    s3_prefix = "step-pipeline"
    region = "us-east-1"
    confirm_changeset = true
    capabilities = "CAPABILITY_IAM"
    parameter_overrides = "S3Bucket=\"blog-step-pipeline-demo\" SNSEndpoint=\"youremailid\" SNSEndpointType=\"email\""
    ~~~~

## Step 5 Validate Application

* Validate the application. or more details please follow this [link](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-validate.html)
  **Command to run:**

    ~~~~aws
    sam validate
    ~~~~

## Step 6 Build Application

* Build the application. For more details please follow this [link](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-build.html).

    **Command to run:**

    ~~~~aws
    sam build
    ~~~~

## Step 7 Deploy Application

* Deploy Application. For more details please follow this [link](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html).
    **Command to run:**

    ~~~~aws
    sam deploy
    ~~~~

    will display the values used for deployment.

    ~~~~aws
    Deploying with following values
	===============================
	Stack name                 : step-pipeline
	Region                     : us-east-1
	Confirm changeset          : True
	Deployment s3 bucket       : blog-step-pipeline-demo
	Capabilities               : ["CAPABILITY_IAM"]
	Parameter overrides        : {'S3Bucket': 'blog-step-pipeline-demo', 'SNSEndpoint': 'youremailid', 'SNSEndpointProtocol': 'email'
    ~~~~

    It will initiate the deployment and upload.

    ~~~~aws
    Initiating deployment
    =====================
    Uploading to step-pipeline/4563ab22057c6195ada5230ff89d4479  7200902 / 7200902.0  (100.00%)
    Uploading to step-pipeline/c7a6fc91b11999f3b1c90dfe05eb8005  7200809 / 7200809.0  (100.00%)
    Uploading to step-pipeline/0927ee565b4ae38859af6b6f9cb721f8  7200628 / 7200628.0  (100.00%)
    Uploading to step-pipeline/e055863aee6da95366b93c06cd84f185  7200758 / 7200758.0  (100.00%)
    Uploading to step-pipeline/d60c001cc0c8a04106a940e38344147e  7204253 / 7204253.0  (100.00%)
    Uploading to step-pipeline/e33924dad68b633c31e08d720a324f99  7200734 / 7200734.0  (100.00%)
    Uploading to step-pipeline/dfd99ba1ae2496f85b8887292ab9fb99  7200707 / 7200707.0  (100.00%)
    Uploading to step-pipeline/b1e626e5230d7094dfdaf49b98370c32  861 / 861.0  (100.00%)
    Uploading to step-pipeline/a94703141e7e92293d32db7559aad1ca  7200660 / 7200660.0  (100.00%)
    Uploading to step-pipeline/3aacadd15742d7e719e130651e82fdaa  7200783 / 7200783.0  (100.00%)
    Uploading to step-pipeline/99137343607be51efba7ad6624feb558  7200688 / 7200688.0  (100.00%)
    Uploading to step-pipeline/b3c6b442d80482459f8b1e2eaa250da7  7200826 / 7200826.0  (100.00%)
    Uploading to step-pipeline/7dd8e4f2511800e09114cd49d1036e6b.template  31417 / 31417.0  (100.00%)

    Waiting for changeset to be created..
    ~~~~

    Next, it will display the CloudFormation stack changeset.

    ~~~~aws
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Operation                                                           LogicalResourceId                                                   ResourceType
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    + Add                                                               AddStepLambdaRole                                                   AWS::IAM::Role
    + Add                                                               AddStepLambda                                                       AWS::Lambda::Function
    + Add                                                               AsyncStartStateMachineLambda                                        AWS::Lambda::Function
    + Add                                                               CFNLambdaRole                                                       AWS::IAM::Role
    + Add                                                               CheckClusterLambda                                                  AWS::Lambda::Function
    + Add                                                               CheckStepLambda                                                     AWS::Lambda::Function
    + Add                                                               CloudFormationRole                                                  AWS::IAM::Role
    + Add                                                               CreateCFNStackLambda                                                AWS::Lambda::Function
    + Add                                                               DeleteCFNStackLambda                                                AWS::Lambda::Function
    + Add                                                               DescribeCFNStackLambda                                              AWS::Lambda::Function
    + Add                                                               FailureLambda                                                       AWS::Lambda::Function
    + Add                                                               GetArrayLengthLambda                                                AWS::Lambda::Function
    + Add                                                               GetClusterIdLambda                                                  AWS::Lambda::Function
    + Add                                                               MLPipelineAlertingSNSTopic                                          AWS::SNS::Topic
    + Add                                                               MLStateMachine                                                      AWS::StepFunctions::StateMachine
    + Add                                                               StartStateMachineLambdaRole                                         AWS::IAM::Role
    + Add                                                               StartStateMachineLambda                                             AWS::Lambda::Function
    + Add                                                               StateMachineRole                                                    AWS::IAM::Role
    + Add                                                               StepFunctionsRole                                                   AWS::IAM::Role
    + Add                                                               SubmitStepStateMachine                                              AWS::StepFunctions::StateMachine
    + Add                                                               SuccessFailureLambdaRole                                            AWS::IAM::Role
    + Add                                                               SuccessLambda                                                       AWS::Lambda::Function
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Changeset created successfully.
    ~~~~

    Next, will ask for deployment confirmation, please enter **Y** if you are agree with the Cloudformation stack changeset, else enter **N** and make the necessary correction.

    ~~~~aws
    Previewing CloudFormation changeset before deployment
    ======================================================
    Deploy this changeset? [y/N]: Y
    ~~~~

    It will update the status of deployment

    ~~~~aws
    2020-04-05 14:30:07 - Waiting for stack create/update to complete

    CloudFormation events from changeset
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ResourceStatus                                     ResourceType                                       LogicalResourceId                                  ResourceStatusReason
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     StateMachineRole                                   Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     CloudFormationRole                                 Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     StartStateMachineLambdaRole                        Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     SuccessFailureLambdaRole                           Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::SNS::Topic                                    MLPipelineAlertingSNSTopic                         Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     AddStepLambdaRole                                  Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     StateMachineRole                                   -
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     CloudFormationRole                                 -
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     SuccessFailureLambdaRole                           -
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     StartStateMachineLambdaRole                        -
    CREATE_IN_PROGRESS                                 AWS::SNS::Topic                                    MLPipelineAlertingSNSTopic                         -
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     AddStepLambdaRole                                  -
    CREATE_COMPLETE                                    AWS::SNS::Topic                                    MLPipelineAlertingSNSTopic                         -
    CREATE_COMPLETE                                    AWS::IAM::Role                                     SuccessFailureLambdaRole                           -
    CREATE_COMPLETE                                    AWS::IAM::Role                                     AddStepLambdaRole                                  -
    CREATE_COMPLETE                                    AWS::IAM::Role                                     StartStateMachineLambdaRole                        -
    CREATE_COMPLETE                                    AWS::IAM::Role                                     CloudFormationRole                                 -
    CREATE_COMPLETE                                    AWS::IAM::Role                                     StateMachineRole                                   -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              CheckClusterLambda                                 -
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     CFNLambdaRole                                      -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              AsyncStartStateMachineLambda                       -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              StartStateMachineLambda                            -
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     CFNLambdaRole                                      Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              FailureLambda                                      -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              AddStepLambda                                      -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              SuccessLambda                                      -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              CheckStepLambda                                    -
    CREATE_COMPLETE                                    AWS::Lambda::Function                              FailureLambda                                      -
    CREATE_COMPLETE                                    AWS::Lambda::Function                              SuccessLambda                                      -
    CREATE_COMPLETE                                    AWS::Lambda::Function                              AsyncStartStateMachineLambda                       -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              AddStepLambda                                      Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              FailureLambda                                      Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              CheckClusterLambda                                 Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              SuccessLambda                                      Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              CheckStepLambda                                    Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              AsyncStartStateMachineLambda                       Resource creation Initiated
    CREATE_COMPLETE                                    AWS::Lambda::Function                              StartStateMachineLambda                            -
    CREATE_COMPLETE                                    AWS::Lambda::Function                              CheckClusterLambda                                 -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              StartStateMachineLambda                            Resource creation Initiated
    CREATE_COMPLETE                                    AWS::Lambda::Function                              AddStepLambda                                      -
    CREATE_COMPLETE                                    AWS::Lambda::Function                              CheckStepLambda                                    -
    CREATE_IN_PROGRESS                                 AWS::StepFunctions::StateMachine                   SubmitStepStateMachine                             -
    CREATE_COMPLETE                                    AWS::StepFunctions::StateMachine                   SubmitStepStateMachine                             -
    CREATE_IN_PROGRESS                                 AWS::StepFunctions::StateMachine                   SubmitStepStateMachine                             Resource creation Initiated
    CREATE_COMPLETE                                    AWS::IAM::Role                                     CFNLambdaRole                                      -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              GetArrayLengthLambda                               -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              DeleteCFNStackLambda                               -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              GetClusterIdLambda                                 -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              DeleteCFNStackLambda                               Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              GetArrayLengthLambda                               Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              CreateCFNStackLambda                               -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              DescribeCFNStackLambda                             -
    CREATE_COMPLETE                                    AWS::Lambda::Function                              DescribeCFNStackLambda                             -
    CREATE_COMPLETE                                    AWS::Lambda::Function                              GetClusterIdLambda                                 -
    CREATE_COMPLETE                                    AWS::Lambda::Function                              DeleteCFNStackLambda                               -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              CreateCFNStackLambda                               Resource creation Initiated
    CREATE_COMPLETE                                    AWS::Lambda::Function                              GetArrayLengthLambda                               -
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              GetClusterIdLambda                                 Resource creation Initiated
    CREATE_IN_PROGRESS                                 AWS::Lambda::Function                              DescribeCFNStackLambda                             Resource creation Initiated
    CREATE_COMPLETE                                    AWS::Lambda::Function                              CreateCFNStackLambda                               -
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     StepFunctionsRole                                  -
    CREATE_IN_PROGRESS                                 AWS::IAM::Role                                     StepFunctionsRole                                  Resource creation Initiated
    CREATE_COMPLETE                                    AWS::IAM::Role                                     StepFunctionsRole                                  -
    CREATE_IN_PROGRESS                                 AWS::StepFunctions::StateMachine                   MLStateMachine                                     -
    CREATE_COMPLETE                                    AWS::StepFunctions::StateMachine                   MLStateMachine                                     -
    CREATE_IN_PROGRESS                                 AWS::StepFunctions::StateMachine                   MLStateMachine                                     Resource creation Initiated
    CREATE_COMPLETE                                    AWS::CloudFormation::Stack                         step-pipeline                                      -
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    CloudFormation outputs from deployed stack
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Outputs
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Key                 GetArrayLengthLambda
    Description         GetArrayLengthLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-GetArrayLengthLambda-1T4XSBG98PC9U

    Key                 CheckStepLambda
    Description         CheckStepLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-CheckStepLambda-RJ52ECLEXAID

    Key                 DescribeCFNStackLambda
    Description         DescribeCFNStackLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-DescribeCFNStackLambda-QFLGOR605OZH

    Key                 CloudFormationRole
    Description         CloudFormationRole ARN
    Value               arn:aws:iam::accountno:role/step-pipeline-CloudFormationRole-EWLP9ZPWQ0OE

    Key                 AddStepLambda
    Description         AddStepLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-AddStepLambda-RCJEBTR16LNY

    Key                 StateMachineRole
    Description         StateMachineRole ARN
    Value               arn:aws:iam::accountno:role/step-pipeline-StateMachineRole-1PFEYND3O1V6

    Key                 AsyncStartStateMachineLambda
    Description         AsyncStartStateMachineLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-AsyncStartStateMachineLambda-YRDJ4C1H6ZU2

    Key                 StepFunctionsRole
    Description         StepFunctionsRole ARN
    Value               arn:aws:iam::accountno:role/step-pipeline-StepFunctionsRole-L91VR6FBYNUU

    Key                 CreateCFNStackLambda
    Description         CreateCFNStackLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-CreateCFNStackLambda-ASPDKV2R2K9C

    Key                 GetClusterIdLambda
    Description         GetClusterIdLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-GetClusterIdLambda-1DGHD479X7XP1

    Key                 FailureLambda
    Description         FailureLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-FailureLambda-V2O9Q61PYHK5

    Key                 CheckClusterLambda
    Description         CheckClusterLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-CheckClusterLambda-1KBKN9R4RZQJP

    Key                 SuccessLambda
    Description         SuccessLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-SuccessLambda-1CG3FUU2D8ME

    Key                 DeleteCFNStackLambda
    Description         DeleteCFNStackLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-DeleteCFNStackLambda-64SSJVO1GS8N

    Key                 StartStateMachineLambda
    Description         StartStateMachineLambda ARN
    Value               arn:aws:lambda:us-east-1:accountno:function:step-pipeline-StartStateMachineLambda-FU1NRX7R3J3N
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Successfully created/updated stack - step-pipeline in us-east-1
    ~~~~

## Step 8 Confirm SNS Notification

* You will get an email from AWS Notification on the specifed email, Please confirm the SNS subscription.

## Step 9 Test Application

* Update your S3 Bucket, Security Group, Sub Net and information in /events/events.JSON
  
  ~~~~JSON
      {
      "ModelName": "Model-Name",
      "ModelProgram": "s3://<your bucket name>/testcode/kmeansandey.py",
      "PreProcessingProgram": "s3://<your bucket name>/testcode/kmeanswsssey.py",
      "EMRCloudFormation": "https://s3.amazonaws.com/<your bucket name>/emr-cluster-sample.yaml",
      "EMRParameters": "https://s3.amazonaws.com/<your bucket name>/emr-cluster-config.json",
      "JobInput": "s3://aws-bigdata-blog/artifacts/anomaly-detection-using-pyspark/sensorinputsmall/",
      "SecurityGroup": "<your-security-group>",
      "SubNet": "< your-subnet>",
      "ClusterSize":"no-of-clusters",
      "ProcessingMode": ["TRAINING"]
      }
      Note: Do not change the JobInput for Demo
  ~~~~

* Go to the [AWS Step Functions](https://console.aws.amazon.com/states/home?/statemachines) console and copy the arn of function named **MLStateMachine**.

* Test AWS Step Functions by submitting an event

  ~~~~ aws
  aws stepfunctions start-execution --state-machine-arn arn:aws:states:<your region>:<your accountid>:stateMachine:awsblog-MLStateMachine-testproject --name test1 --input file://events/event.json
  ~~~~

* You should now be able to view the step function initiated, the new EMR cluster created and the steps executed. Once the process is completed you will be able to see the output in `<your bucket name>/output/`.


## License

This library is licensed under the MIT-0 License. See the LICENSE file.

