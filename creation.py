import boto3
import os
import re
import json

# def get_s3_file(sts, bucket_name):
#   s3 = sts.resource('s3')
#   bucket = s3.Bucket(bucket_name)
#   object_summary = bucket.objects.all()
#   for object in object_summary:
#     re_match = re.compile('org/cross-account/securitygroups/jcrew-it-support-sg.json')
#     if re_match.match(object.key):
#       body = object.get()['Body'].read()
#       if body:
#         return json.loads(body)

# Paginate function
def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result

def lambda_handler(event, context):
  #accounts_to_exclude = os.environ.get('accounts_to_exclude')
  organization_service_role = os.environ.get('organization_service_role')
  sts_role_session_name = os.environ.get('sts_role_session_name')
  account = event['account']
  session = boto3.Session(region_name='us-east-1')
  org_session = session.client('organizations')
  regions = [regions['RegionName'] for regions in session.client('ec2').describe_regions()['Regions']]
 
  #IpPermissions = get_s3_file(session, bucket_name)
  
  # Iterate through sub accounts
  sts_client = session.client('sts')
  print('Processing account', account, ':')

  for region in regions:

 ##############################################################################################################
 ##############################################################################################################
      # # Use STS to assume a temporary role in the sub account that has the Organization service role.
      # # If the sub account does not have the Organization service role it will be excepted.
      try:
        role_arn = 'arn:aws:iam::' + account + ':role/' + organization_service_role
        sts_response = sts_client.assume_role(
          RoleArn=role_arn,
          RoleSessionName=sts_role_session_name,
          DurationSeconds=900
        )
        # Create boto3 session for account.
        sts_session = boto3.Session(
          aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
          aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
          aws_session_token=sts_response['Credentials']['SessionToken'],
         region_name=region
       )
      except:
      # If sub account does not have Organization service role we log it and ignore the account.
        sts_session = ''
        print('failed to assume role for account', account)
        break
      # else:
      #   sts_session = session 
      
  ##############################################################################################################
  ##############################################################################################################

      if sts_session != '':
          s3_client = sts_session.client('s3', region_name=region)

          print('Processing account', account, " and region ", region)
        
          
      

          bucket_list = s3_client.list_buckets()
          for bucket in bucket_list['Buckets']:
              try:
                  lifecycle = s3_client.get_bucket_lifecycle(Bucket=bucket['Name'])
                  rules = lifecycle['Rules']
                
              except:
                  rules = 'No Policy'
                  print(bucket,['Name'], rules) 