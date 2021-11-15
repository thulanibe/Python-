import logging
import boto3
import datetime, os, json, boto3
from botocore.exceptions import ClientError
from pprint import pprint

regions = ['us-east-1']

def lambda_handler(event, context):
    

    organization_service_role = 'OrganizationAccountAccessRole'
    sts_role_session_name = 'org-session'
    aws_region = os.environ.get('aws_region')
    regions = [regions['RegionName'] 
    #org_session = session.client('organizations')
    org_client = session.client('organizations')
    session = boto3.Session(region_name=aws_region)
    for regions in session.client('ec2').describe_regions()['Regions']]
    s3 = boto3.client('s3')
    response = s3.list_buckets()

     




    for region in regions:

    
    # Output the bucket names
      print('Existing buckets:')
    for bucket in response['Buckets']:
        #print(f'  {bucket["Name"]}')
        if 'log' in bucket['Name']:
            BUCKET = bucket["Name"]
            print (BUCKET)
            try:
                policy_status = s3.put_bucket_lifecycle_configuration(
                          Bucket = BUCKET ,
                          LifecycleConfiguration={'Rules': [{'Expiration':{'Days': 30,'ExpiredObjectDeleteMarker': True},'Status': 'Enabled',} ]})
            except ClientError as e:
                 print("Unable to apply bucket policy. \nReason:{0}".format(e))