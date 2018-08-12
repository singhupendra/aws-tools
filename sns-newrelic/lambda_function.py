'''
This is a basic lamdbda function which recieves data from new relic and sends you a SMS
'''
import requests
import json
import boto3

def lambda_handler(event, context):
    TopicArn = "{YOUR SNS TOPIC ARN}"
    region = "{YOUR TOPIC REGION}"
    message = json.dumps(event)
    message = json.loads(message)
    text = message['condition_name'] + ' ' + message['incident_url'] + ' ' + message['severity'] + ' ' + message['details']
    client = boto3.client('sns',region_name=region)
    response = client.publish(TargetArn=TopicArn,Message=text)
    return "success"
