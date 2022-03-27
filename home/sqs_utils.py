import boto3
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
import os
# Import the file that has the environment variables
if os.path.exists("env.py"):
    import env as env_variables

class SqsQueue:

    def create_and_consume_queue(request, queue_name):
        try:
            sqs_client = boto3.client('sqs', region_name=env_variables.get_aws_region("aws_educate"), aws_access_key_id=env_variables.get_aws_access_key("aws_educate"), 
                                            aws_secret_access_key=env_variables.get_aws_secret_key("aws_educate"), 
                                            aws_session_token=env_variables.get_aws_session_token("aws_educate"))
            print(f"Creating the {queue_name} queue")
            if queue_name == "display_home_page":
                template = loader.get_template('home/templates/index.html')
                return HttpResponse(template.render({},request))
        except Exception as e:
            print(e) 

            



            
