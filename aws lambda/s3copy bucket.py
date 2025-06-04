import boto3 

print('copy all files greater than threhold size')
src_bucket = 'source-bucket'
s3 = boto3.resource('s3')

for bucket in s3.buckets.all():][p]
    print('Copy all ilke greater thsan the threshold from one bucket to another')
    src_bucket_name = input('Enter source bucket name')
    des_bucket_name = input('Enter destination bucket name')
    file_size = float(input('Enter threshold size in mb')) * 1000000
    
    copied_files = 0
    
    src_bucket = s3.Bucket(src_bucket_name)
    for item in src_bucket.object_all():
        if item.size > file_size:
            s3.meta.client.copy_object(
                Bucket = des_bucket_name,
                Key = item.key,
                CopySource = f'{src_bucket_name}/{item.key}'
            )
            copied_files += 1
            s3.meta.client.delete_object(
                Bucket = dest_bucket_name,
                CopySource = {'Bucket' = {src_bucket_name}/{item.key}',
                Key = item.key
            )
            
            print('\nFiles copied:' + str(copied_files))
    