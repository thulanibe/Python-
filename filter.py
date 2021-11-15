import boto3

#boto3.setup_default_session(profile_name='my_profile')
client = boto3.client('s3')
# get list of buckets this iam role can see
buckets = client.list_buckets()['Buckets']

# iterate through list of buckets looking at tags
matching_buckets = []
# tag key and value to search for
tag_key = 'test'
tag_value = '442'

for idx, bucket in enumerate(buckets):
#comment out following line if you don't want to see the progress
#print(f'{idx+1} of {len(buckets)} - {bucket["Name"]}')

    try:
        tags = client.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']
    except client.exceptions.ClientError:
        continue
    # iterate through tags looking for specific key
    for tag in tags:
        if tag['Key'] == tag_key and tag['Value'] == tag_value:
            matching_buckets.append(bucket['Name'])

print("buckets belonging to", tag_value, "are: ", matching_buckets)