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
                                        aws_session_token="FwoGZXIvYXdzEAIaDLZmCOn1/5yAEQRQciLLAeJc1xErMTQMJOnnMib/Nh424cUjq1nM5abgy+InX0aaIzBg0tG4843vcCB7DnM+CjuIzOCrs52ufT0idBvqibGxyexAG7bGdDyMJLdS6/Ef1/+NslUEhWbhVkcMfjDA9xZxl46aLIORZG46pPQNu1rkc7MSDcvGnLSHY2TK99p3dQ0uAypPuQZu0YiPNHtzHors+soXn3s+i6+P7blnec0135NHEHZBv1iPgDCj8ceGL0TwqwSpd5kE7+onz5BgcP+dteQH4KDh141cKLizv5EGMi1LO1noebm7CQzXCtZrq8yhUHIFGVi5JRQ4Xo1ZLIqH8SgNSeoyVJPFdbGEfdU=")
            response = sns_client.create_topic(Name=topic_name)
            topic_arn = response['TopicArn']
            sns_client.subscribe(TopicArn=topic_arn, Protocol = 'email', Endpoint = user_email)
        except ClientError as e:
            logging.error(e)
            print("An isue occured subscribing")
            return