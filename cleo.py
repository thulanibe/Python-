import boto3

s3_client = boto3.client('s3')

bucket_list = s3_client.list_buckets()

for bucket in bucket_list['Buckets']:
    bucket_with_no_policy=[]
    try:
        lifecycle = s3_client.get_bucket_lifecycle(Bucket=bucket['Name'])
        rules = lifecycle['Rules']
    except:
        rules = 'jcrew-default-s3-lifecycle'

    if rules != 'Policy':
        bucket_with_no_policy.append(bucket['Name'])
        print(bucket_with_no_policy + rules)

