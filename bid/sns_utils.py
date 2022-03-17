import boto3
from botocore.exceptions import ClientError
import logging
import os
# Import the file that has the environment variables
if os.path.exists("env.py"):
    import env as env_variables

class sns:

    @staticmethod
    def topic_subscribe(topic_name, user_email):
        try:
            sns_client = boto3.client('sns', region_name=env_variables.get_aws_region("aws_educate"), aws_access_key_id=env_variables.get_aws_access_key("aws_educate"), 
                                        aws_secret_access_key=env_variables.get_aws_secret_key("aws_educate"), 
                                        aws_session_token=env_variables.get_aws_session_token("aws_educate"))
            response = sns_client.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            sns_client.subscribe(TopicArn=topic_arn, Protocol = 'email', Endpoint = user_email)
        except ClientError as e:
            logging.error(e)
            print("An isue occured subscribing")

    @staticmethod
    def publish_new_bid(topic_name, message):
        try:
            sns_client = boto3.client('sns', region_name=env_variables.get_aws_region("aws_educate"), aws_access_key_id=env_variables.get_aws_access_key("aws_educate"), 
                                            aws_secret_access_key=env_variables.get_aws_secret_key("aws_educate"), 
                                            aws_session_token=env_variables.get_aws_session_token("aws_educate"))
            # Try to publish the message
            response = sns_client.create_topic(Name = topic_name)
            topic_arn = response['TopicArn']
            try:
                response = sns_client.publish(TopicArn = topic_arn, Message = message)
            except Exception as e:
                print(e)
        except ClientError as e:
            logging.error(e)
            print("An isue occured in the message publish process")