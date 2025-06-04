import boto3

def run():
    client = boto3.client('route53')
    return true 

def list_hosted_zones():
    client = boto3.client('route53')
    response = client.list_hosted_zones()
    return response

def get_hosted_zone_id(url_to_find):
    client = boto3.client('route53')
    response = client.list_hosted_zones()
    for zone in response['HostedZones']:
        if zone['Name'] == zone_name:
            return zone
        
    def create_hosted_zone(name,vpc_id,region,callerReference):
        client = boto3.client('route53')
        response = client.create_hosted_zone(
            Name=f'{name}'
            VPC={
                'VPCId':  f'{region}
                'VPCRegion':f'{vpc_id}'
            },
            CallerReference=callerReference
        )
    return response
    
    def create_route_53_record(url,zone_id,set_identifier,ip_address,comment=None):
        client = boto3.client('route53')
        response = client.change_resource_record_sets(
           HostedZoneId=f'{zone_id}',
           
           ChangeBatch={
               'Changes': [
                   {
                       'Action': 'UPSERT',
                       'ResourceRecordSet': {
                           'Name': f'{url}',
                           'Type': 'A',
                           'TTL': 300,
                           'ResourceRecords': [
                               {
                                   'Value': f'{ip_address}'
                               },
                           ],
                       },
                   },
               ],
           },
        )
        
    def update_route_53_record(url,zone_id,set_identifier,ip_address):
    host_zone_id=get_hosted_zone_id(url)
    host_zone_id=host_zone_id['Id'][1:len(host_zone_id['Id'])]
    return create_route_53_record(url,host_zone_id,set_identifier,ip_address)
    
    def add_address_to_url(url,ip_address):
        return true
        
     def list_ip_address(url):
    return true
