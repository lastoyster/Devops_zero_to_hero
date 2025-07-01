import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError
from typing import List, Dict, Any

def get_s3_client():
    """Create and return S3 client with error handling"""
    try:
        return boto3.client('s3')
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        return None

def get_ec2_client():
    """Create and return EC2 client with error handling"""
    try:
        return boto3.client('ec2')
    except NoCredentialsError:
        print("Error: AWS credentials not found. Please configure your credentials.")
        return None

def check_bucket_public_access(s3_client, bucket_name: str) -> Dict[str, Any]:
    """Check if a bucket has public access configurations"""
    try:
        # Check public access block
        try:
            public_access_block = s3_client.get_public_access_block(Bucket=bucket_name)
            pab = public_access_block['PublicAccessBlockConfiguration']
            has_public_block = all([
                pab.get('BlockPublicAcls', False),
                pab.get('IgnorePublicAcls', False),
                pab.get('BlockPublicPolicy', False),
                pab.get('RestrictPublicBuckets', False)
            ])
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                has_public_block = False
            else:
                raise
        
        # Check bucket policy for public access
        has_public_policy = False
        try:
            policy = s3_client.get_bucket_policy(Bucket=bucket_name)
            policy_doc = json.loads(policy['Policy'])
            
            # Check for policies that allow public access
            for statement in policy_doc.get('Statement', []):
                principal = statement.get('Principal', {})
                if principal == '*' or (isinstance(principal, dict) and principal.get('AWS') == '*'):
                    has_public_policy = True
                    break
        except ClientError as e:
            if e.response['Error']['Code'] != 'NoSuchBucketPolicy':
                raise
        
        # Check bucket ACL
        has_public_acl = False
        try:
            acl = s3_client.get_bucket_acl(Bucket=bucket_name)
            for grant in acl.get('Grants', []):
                grantee = grant.get('Grantee', {})
                if grantee.get('Type') == 'Group':
                    uri = grantee.get('URI', '')
                    if 'AllUsers' in uri or 'AuthenticatedUsers' in uri:
                        has_public_acl = True
                        break
        except ClientError:
            pass
        
        is_secure = has_public_block and not has_public_policy and not has_public_acl
        
        return {
            'bucket_name': bucket_name,
            'is_secure': is_secure,
            'has_public_block': has_public_block,
            'has_public_policy': has_public_policy,
            'has_public_acl': has_public_acl
        }
    
    except ClientError as e:
        print(f"Error checking bucket {bucket_name}: {e}")
        return None

def list_insecure_s3_buckets() -> List[str]:
    """List all S3 buckets that have insecure (public) access"""
    s3_client = get_s3_client()
    if not s3_client:
        return []
    
    try:
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        insecure_buckets = []
        
        print("Checking bucket security configurations...")
        for bucket in buckets:
            bucket_name = bucket['Name']
            bucket_info = check_bucket_public_access(s3_client, bucket_name)
            
            if bucket_info and not bucket_info['is_secure']:
                insecure_buckets.append(bucket_name)
                print(f"  - {bucket_name}: INSECURE")
                if bucket_info['has_public_policy']:
                    print(f"    * Has public bucket policy")
                if bucket_info['has_public_acl']:
                    print(f"    * Has public ACL")
                if not bucket_info['has_public_block']:
                    print(f"    * Missing public access block")
        
        return insecure_buckets
    
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return []

def disable_insecure_s3_bucket_access(bucket_name: str) -> bool:
    """Disable insecure access to an S3 bucket by applying public access block"""
    s3_client = get_s3_client()
    if not s3_client:
        return False
    
    try:
        # Apply comprehensive public access block
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
        print(f"Successfully applied public access block to bucket: {bucket_name}")
        return True
    
    except ClientError as e:
        print(f"Error applying public access block to bucket {bucket_name}: {e}")
        return False

def list_secure_s3_buckets() -> List[str]:
    """List all S3 buckets that have secure (non-public) access"""
    s3_client = get_s3_client()
    if not s3_client:
        return []
    
    try:
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])
        secure_buckets = []
        
        print("Checking bucket security configurations...")
        for bucket in buckets:
            bucket_name = bucket['Name']
            bucket_info = check_bucket_public_access(s3_client, bucket_name)
            
            if bucket_info and bucket_info['is_secure']:
                secure_buckets.append(bucket_name)
                print(f"  - {bucket_name}: SECURE")
        
        return secure_buckets
    
    except ClientError as e:
        print(f"Error listing buckets: {e}")
        return []

def enable_secure_s3_bucket_access(bucket_name: str) -> bool:
    """Enable secure access to an S3 bucket (same as disable_insecure_s3_bucket_access)"""
    return disable_insecure_s3_bucket_access(bucket_name)

def delete_all_objects_in_bucket(bucket_name: str) -> bool:
    """Delete all objects in an S3 bucket (with confirmation)"""
    s3_client = get_s3_client()
    if not s3_client:
        return False
    
    try:
        # Double confirmation for destructive operation
        print(f"WARNING: This will delete ALL objects in bucket '{bucket_name}'")
        confirm1 = input("Are you sure you want to continue? (type 'yes' to confirm): ")
        if confirm1.lower() != 'yes':
            print("Operation cancelled.")
            return False
        
        confirm2 = input(f"Type the bucket name '{bucket_name}' to confirm: ")
        if confirm2 != bucket_name:
            print("Bucket name mismatch. Operation cancelled.")
            return False
        
        # List and delete all objects
        paginator = s3_client.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name)
        
        objects_deleted = 0
        for page in pages:
            if 'Contents' in page:
                objects = [{'Key': obj['Key']} for obj in page['Contents']]
                if objects:
                    s3_client.delete_objects(
                        Bucket=bucket_name,
                        Delete={'Objects': objects}
                    )
                    objects_deleted += len(objects)
        
        # Also delete any versioned objects
        paginator = s3_client.get_paginator('list_object_versions')
        pages = paginator.paginate(Bucket=bucket_name)
        
        for page in pages:
            versions = []
            if 'Versions' in page:
                versions.extend([{'Key': v['Key'], 'VersionId': v['VersionId']} for v in page['Versions']])
            if 'DeleteMarkers' in page:
                versions.extend([{'Key': dm['Key'], 'VersionId': dm['VersionId']} for dm in page['DeleteMarkers']])
            
            if versions:
                s3_client.delete_objects(
                    Bucket=bucket_name,
                    Delete={'Objects': versions}
                )
                objects_deleted += len(versions)
        
        print(f"Successfully deleted {objects_deleted} objects from bucket: {bucket_name}")
        return True
    
    except ClientError as e:
        print(f"Error deleting objects from bucket {bucket_name}: {e}")
        return False

def list_ec2_instances() -> List[Dict[str, Any]]:
    """List all EC2 instances with their details"""
    ec2_client = get_ec2_client()
    if not ec2_client:
        return []
    
    try:
        response = ec2_client.describe_instances()
        instances = []
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_info = {
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name'],
                    'LaunchTime': instance['LaunchTime'],
                    'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
                    'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
                    'VpcId': instance.get('VpcId', 'N/A'),
                    'SubnetId': instance.get('SubnetId', 'N/A')
                }
                
                # Get instance name from tags
                name = 'N/A'
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break
                instance_info['Name'] = name
                
                instances.append(instance_info)
        
        return instances
    
    except ClientError as e:
        print(f"Error listing EC2 instances: {e}")
        return []

def stop_ec2_instances(instance_ids: List[str]) -> bool:
    """Stop specified EC2 instances"""
    ec2_client = get_ec2_client()
    if not ec2_client:
        return False
    
    try:
        # Clean up instance IDs (remove whitespace)
        instance_ids = [id.strip() for id in instance_ids if id.strip()]
        
        if not instance_ids:
            print("No valid instance IDs provided.")
            return False
        
        print(f"Attempting to stop instances: {', '.join(instance_ids)}")
        
        response = ec2_client.stop_instances(InstanceIds=instance_ids)
        
        print("Stop request sent successfully:")
        for instance in response['StoppingInstances']:
            print(f"  - {instance['InstanceId']}: {instance['PreviousState']['Name']} -> {instance['CurrentState']['Name']}")
        
        return True
    
    except ClientError as e:
        print(f"Error stopping EC2 instances: {e}")
        return False

def display_menu():
    """Display the main menu"""
    print("AWS Security Checker Menu:")
    print("1. List Insecure S3 Buckets")
    print("2. Disable Insecure S3 Bucket Access")
    print("3. List Secure S3 Buckets")
    print("4. Enable Secure S3 Bucket Access")
    print("5. Delete All Objects in a Bucket")
    print("6. List EC2 Instances")
    print("7. Stop EC2 Instances")
    print("8. Exit")

def display_disclaimer():
    """Display the disclaimer"""
    print("*** DISCLAIMER ***")
    print("This script interacts with your AWS account and can make changes to your resources.")
    print("Ensure that you have the necessary permissions and use it responsibly.")
    print("The script is provided as-is without any warranty. Use at your own risk.")
    print("Make sure your AWS credentials are properly configured (AWS CLI, environment variables, or IAM roles).")

def main():
    """Main function to run the AWS Security Checker"""
    display_disclaimer()
    print()
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            print("\n--- Listing Insecure S3 Buckets ---")
            insecure_buckets = list_insecure_s3_buckets()
            if insecure_buckets:
                print(f"\nFound {len(insecure_buckets)} insecure bucket(s):")
                for bucket in insecure_buckets:
                    print(f"  - {bucket}")
            else:
                print("No insecure buckets found or unable to check buckets.")
                
        elif choice == '2':
            print("\n--- Disable Insecure S3 Bucket Access ---")
            bucket_name = input("Enter the name of the bucket to disable insecure access: ").strip()
            if bucket_name:
                success = disable_insecure_s3_bucket_access(bucket_name)
                if success:
                    print("✓ Insecure access disabled successfully.")
                else:
                    print("✗ Failed to disable insecure access.")
            else:
                print("No bucket name provided.")
                
        elif choice == '3':
            print("\n--- Listing Secure S3 Buckets ---")
            secure_buckets = list_secure_s3_buckets()
            if secure_buckets:
                print(f"\nFound {len(secure_buckets)} secure bucket(s):")
                for bucket in secure_buckets:
                    print(f"  - {bucket}")
            else:
                print("No secure buckets found or unable to check buckets.")
                
        elif choice == '4':
            print("\n--- Enable Secure S3 Bucket Access ---")
            bucket_name = input("Enter the name of the bucket to enable secure access: ").strip()
            if bucket_name:
                success = enable_secure_s3_bucket_access(bucket_name)
                if success:
                    print("✓ Secure access enabled successfully.")
                else:
                    print("✗ Failed to enable secure access.")
            else:
                print("No bucket name provided.")
                
        elif choice == '5':
            print("\n--- Delete All Objects in a Bucket ---")
            bucket_name = input("Enter the name of the bucket to delete all objects: ").strip()
            if bucket_name:
                success = delete_all_objects_in_bucket(bucket_name)
                if success:
                    print("✓ All objects deleted successfully.")
                else:
                    print("✗ Failed to delete objects or operation cancelled.")
            else:
                print("No bucket name provided.")
                
        elif choice == '6':
            print("\n--- Listing EC2 Instances ---")
            instances = list_ec2_instances()
            if instances:
                print(f"\nFound {len(instances)} instance(s):")
                print(f"{'Instance ID':<20} {'Name':<25} {'Type':<15} {'State':<15} {'Public IP':<15}")
                print("-" * 90)
                for instance in instances:
                    print(f"{instance['InstanceId']:<20} {instance['Name']:<25} {instance['InstanceType']:<15} {instance['State']:<15} {instance['PublicIpAddress']:<15}")
            else:
                print("No instances found or unable to list instances.")
                
        elif choice == '7':
            print("\n--- Stop EC2 Instances ---")
            instance_ids_input = input("Enter the comma-separated list of EC2 instance IDs to stop: ").strip()
            if instance_ids_input:
                instance_ids = [id.strip() for id in instance_ids_input.split(',') if id.strip()]
                if instance_ids:
                    success = stop_ec2_instances(instance_ids)
                    if success:
                        print("✓ Stop request sent successfully.")
                    else:
                        print("✗ Failed to stop instances.")
                else:
                    print("No valid instance IDs provided.")
            else:
                print("No instance IDs provided.")
                
        elif choice == '8':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please enter a number from 1 to 8.")
        
        print()

if __name__ == "__main__":
    main()