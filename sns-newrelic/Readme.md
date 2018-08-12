This a function to receive and process webhook from new relic and send you SMS using AWS SNS service.


Requirement
1. AWS API Gateway endpoint with a POST method allowed
2. API Gateway should be able to invoke the lambda function
3. IAM role for lamnda function to publish SMS from your SNS topic
4. webhook notification channel in new relic to send data to AWS API Gateway
