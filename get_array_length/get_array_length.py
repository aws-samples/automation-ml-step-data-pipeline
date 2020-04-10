from __future__ import print_function
from _datetime import datetime
import json

def lambda_handler(event, context):

    print("lambda_handler:Starting process")
    print("lambda_handler:Return length of array")
    print("lambda_handler:Event is:" + str(event))

    processing_mode = []
    processing_mode = event['processing_mode']

    return(len(processing_mode))