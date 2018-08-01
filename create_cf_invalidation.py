'''
This is a lambda function which can be triggered whenever there is a change in your desired s3 bucket
'''

'''
Needs IAM Role with below policies policy

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
    {
        "Effect": "Allow",
        "Action": [
            "cloudfront:CreateInvalidation"
        ],
        "Resource": [
            "*"
        ]
    }
  ]
}

'''

from __future__ import print_function

import boto3
import time
import requests
DistributionId='Your CF DistributionId'
webhook_url="Your Slack webhook_url"

def lambda_handler(event, context):
    path = []
    for items in event["Records"]:
        if items["s3"]["object"]["key"] == "index.html":
            path.append("/")
        else:
            path.append("/" + items["s3"]["object"]["key"])
    print(path)
    client = boto3.client('cloudfront')
    invalidation = client.create_invalidation(DistributionId=DistributionId,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': path
        },
        'CallerReference': str(time.time())
    })
    slack(path)

def slack (path):
    slack_data = {'text': "created cloudfront invalidation for url " + data}

    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )
