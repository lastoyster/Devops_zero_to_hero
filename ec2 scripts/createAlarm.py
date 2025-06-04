import boto3

cloudwatch = boto3.client('cloudwatch')

    alarm_name='test-alarm',
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=60,
    Statistic='Average',
    Threshold=50.0,
    ActionsEnabled=True,
    AlarmDescription='This metric monitors ec2 cpu utilization',
    Period=period,
    Statistic='Average',
    Threshold=threshold,
    AlarmDescription=alarm_description,
    )
    
    print("Alarm created: ",    response)