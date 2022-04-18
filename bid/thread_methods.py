from asyncio import Queue
from .sns_utils import sns
from .models import Bid
from property.models import Property
import boto3
from botocore.exceptions import ClientError
import logging
import os
# Import the file that has the environment variables
if os.path.exists("env.py"):
    import env as env_variables

def sns_topic_creator(request, thread_list):
    # Try to create a sns topic for the property
    try:
        # The property index will be 0 and index 1 will track if sns was successfully created/subscribed or not
        sns.topic_subscribe(f"BidNotificationForPropertyId{thread_list[0]}", request.session['cognito_details']['email'])
        thread_list[1] = True
    except Exception as e:
        thread_list[1] = False
        print(e)

def bid_creator(request, thread_list):
    try:
        # Check if the bidder already has a bid on the property
        if Bid.objects.filter(property=Property.objects.get(pk=thread_list[1])).filter(user = request.session['cognito_details']['email']):
            # Get the users existing bid and update with new bid value
            try:
                # The property id will always be index 1 in the list parameter
                bid = Bid.objects.get(property=Property.objects.get(pk=thread_list[1]), user = request.session['cognito_details']['email'])
                bid.amount = float(request.POST.get('bid_amount'))
                bid.save()
                thread_list[0] = True
            except Exception as e:
                print("Error Here")
                print(e)
        else:
            try:
                # If the bidder doesn't already have a bid for the property instantiate the Bid class
                Bid.objects.create_bid(Property.objects.get(pk=thread_list[1]), request.session['cognito_details']['email'], float(request.POST.get('bid_amount')))
                thread_list[0] = True
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

def publish_new_bid(request, property_id):
    try:
        # Get the correct property from property_id argument
        sqs_message = f"BidNotificationForPropertyId{property_id[0]}"+"##"+f"There has just been a new bid of €{request.POST.get('bid_amount')} on the property at:\n{property.address.house_number} {property.address.street},\n{property.address.town},\n{property.address.county}"
        queue_url = "https://sqs."+env_variables.get_aws_region("aws_educate")+".amazonaws.com/"+env_variables.get_aws_account_id("aws_educate")+"/BidNotificationQueue"
        
        sqs_client = queue_client()
        sqs_client.send_message(
            QueueUrl = queue_url,
            MessageBody = sqs_message
        )

        response = sqs_client.receive_message(
            QueueUrl = queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessage=1
        )

        queue_message = response['Message']
        snsParams = queue_message.split("##")

        property = Property.objects.get(pk=property_id[0])
        sns.publish_new_bid(snsParams[0], snsParams[1])
        # Index 1 at property_id list argument is a False boolean. Adjust boolean to True if successful publish
        property_id[1] = True
    except Exception as e:
        property_id[1] = False
        print(f"Test here: \n{e}")


def create_queue():
    try:
        # Create SQS Queue to send all the messages
        sqs_client = queue_client()
        queue = sqs_client.create_queue(Name="BidNotificationQueue")
        return queue
    except ClientError as e:
        logging.error(e)
        print("An isue occured while creating the queue")

def queue_client():

    try:
        # SQS Client
        sqs_client = boto3.client('sqs', region_name=env_variables.get_aws_region("aws_educate"), aws_access_key_id=env_variables.get_aws_access_key("aws_educate"), 
                                    aws_secret_access_key=env_variables.get_aws_secret_key("aws_educate"), 
                                    aws_session_token=env_variables.get_aws_session_token("aws_educate"))
        return sqs_client
    except ClientError as e:
        logging.error(e)
        print("An isue occured while creating the queue client")
    


       