
from copy import error
import boto3
import os
import re
import json
from botocore.exceptions import ClientError
import io
# import pytest


s3=boto3.client("s3")
s3_client=boto3.client("s3")


client = boto3.client('s3')

regions = ['us-east-1,us-west-2']

    # Paginate function
def paginate(method, **kwargs):
        client = method.__self__
        paginator = client.get_paginator(method.__name__)
        for page in paginator.paginate(**kwargs).result_key_iters():
          for result in page:
           yield result

def lambda_handler(event, context):

 
  role_arn =  'arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
  sts_role_session_name = 'org-session'
    
  session = boto3.Session(region_name='us-east-1')
  org_client = session.client('organizations')
  regions = 'regions'


    # Get list of ACTIVE accounts in the organization, this list contains only accounts that have been created or accepted
    # an invitation to the organization.  This list will also contain those accounts without the Organization service role.

  org_accounts=[]
  for key in paginate(org_client.list_accounts):
    if key['Status'] == 'ACTIVE':
      org_accounts.append(str(key['Id']))

  result = {}
  all_hosts = []

  
  org_accounts = ['335418536307','513057034381','8355366714']
  

  for account in org_accounts:
      #iterate through sub accounts
      sts_client = session.client('sts')
      
  #regions = ['us-east-1']
  for region in regions :
      try:
            role_arn =  'arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
            sts_response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=sts_role_session_name,
            DurationSeconds=90
            )
            response = sts_client.get_caller_identity()
            print(response)


            # Create boto3 session for account.
            sts_session = boto3.Session(
            aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
            aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
            aws_session_token=sts_response['Credentials']['SessionToken'],
            # region_name=region
            )
      except:
                # If sub account does not have Organization service role we log it and ignore the account.
                sts_session = ''
                print('failed to assume role for account', account)
            
      else:
           sts_session = session 

    ##############################################################################################################
    ##############################################################################################################

      if sts_session != '':

        info = []
        
            #### Code to execute against all regions in every account
        s3_client = sts_session.client('s3', region_name=region)
        print('Processing account', account, " and region ", region)
                
        # Retrieve the policy of the specified buckets and indicate no policy for buckets without life cycle policy 
            
        s3_client = boto3.client('s3') 
            
        bucket_list = s3_client.list_buckets()

        for bucket in bucket_list['Buckets']:

            try:
                lifecycle = s3_client.get_bucket_lifecycle(Bucket=bucket['Name'],DryRun=True)
                rules = lifecycle ['Rules']
            except ClientError as e:
              if 'DryRunOperation' not in str(e):
                rules = 'No Policy'
            print(bucket['Name'], rules)
            raise
 

        #list the names of the bucket without policy
        bucket_list = s3_client.list_buckets()

        for bucket in bucket_list['Buckets']:
            bucket_with_no_policy=[]
            try:
                lifecycle = s3_client.get_bucket_lifecycle(Bucket=bucket['Name'],DryRun=False)
                rules = lifecycle['Rules']
            except ClientError as e:
                rules = 'No Policy'

            if rules == 'No Policy':
                bucket_with_no_policy.append(bucket['Name'])
                print(bucket_with_no_policy)
                print('Error', e)






lambda_handler(
  {
    'action': 'run'
  },
  'context'
)