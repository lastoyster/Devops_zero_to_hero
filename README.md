# Devops_zero_to_hero

EC2 Tag Notification
Automated notifications when EC2 Instances are missing a specific tag

Steps:
Create an SNS Topic for Email Notifications
Go to the Amazon SNS Console and create a topic (e.g., MissingTagNotifications).
Choose the topic type as Standard.
Give it a name and create the topic.
Create a subscription to this SNS topic with your email address, and confirm the subscription via the email you receive.
Create a Lambda Function to Check EC2 Instances
Go to the AWS Lambda Console and create a new Lambda function.
Choose "Author from scratch," give it a name (e.g., CheckEC2Tags), and use a Python runtime.
Attach the necessary permissions to the Lambda function:
EC2 DescribeInstances permission to read instance tags.
SNS Publish permission to send notifications.
Here's a sample Python code for the Lambda function:

import boto3
import os

ec2 = boto3.client('ec2')
sns = boto3.client('sns')

def lambda_handler(event, context):
    # Replace with your SNS topic ARN
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']
    
    # Describe EC2 instances
    instances = ec2.describe_instances()
    
    missing_tag_instances = []
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            # Get tags
            tags = instance.get('Tags', [])
            # Check if the 'Environment' tag is missing or empty
            if not any(tag['Key'] == 'Environment' and tag['Value'] for tag in tags):
                missing_tag_instances.append(instance['InstanceId'])
    
    # If any instances are missing the 'Environment' tag, send an SNS notification
    if missing_tag_instances:
        message = f"These EC2 instances are missing the 'Environment' tag: {missing_tag_instances}"
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject="EC2 Instances Missing 'Environment' Tag",
            Message=message
        )
    
    return {
        'statusCode': 200,
        'body': 'Notification sent for missing tag instances.'
    }

Configure Lambda Environment Variables
After creating the Lambda function, set the following environment variable:
SNS_TOPIC_ARN: Set this to the ARN of the SNS topic created earlier.
Create a CloudWatch Rule (EventBridge)
Go to the CloudWatch Console and create a rule.
Select Event Source as EventBridge and choose a schedule (e.g., every five minutes).
To run the EventBridge rule every 5 minutes, you can use the following cron expression:
cron(0/5 * * * ? *)
Set the target as the Lambda function you created (CheckEC2Tags).
Test the Solution You can either manually run the Lambda function from the console to verify that it is checking for instances without the tag or wait for the CloudWatch rule to trigger the Lambda function based on your schedule. If any instances are missing the required Environment tag or its value, you will receive an email notification listing the instance IDs.
YouTube Video: Automate EC2 Tag Monitoring with AWS EventBridge and Lambda | Real-Time Notifications Setup
In this video, we walk you through setting up an automated solution to monitor your EC2 instances and ensure they have the required tags (like Environment). Using AWS EventBridge, Lambda, and SNS, we demonstrate how to get notified via email if any EC2 instance is missing a specific tag. Learn how to create a scheduled rule that runs every 5 minutes and keeps your infrastructure compliant!

What you’ll learn:

Setting up an AWS Lambda function to check EC2 instances for missing tags.
Scheduling automatic checks using AWS EventBridge with a cron expression.
Configuring Amazon SNS to send email notifications.
Ensuring proper tagging for better cost and resource management in AWS.
Stay tuned for this hands-on tutorial and simplify your AWS management!
#AWS #CloudAutomation #EC2Monitoring #LambdaFunction #EventBridge #TagCompliance #CloudWatch #DevOps #CloudComputing #AWSTutorial #CloudInfrastructure
