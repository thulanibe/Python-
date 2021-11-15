import boto3
import os
import re
import json

# regions = []

regions = ['us-east-1']

 
   


# Paginate function
def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result

def lambda_handler(event, context):
 
role_arn = ' arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
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

 
org_accounts = ['917848291101']

for account in org_accounts:
    #iterate through sub accounts
 sts_client = session.client('sts')
     
 regions = ['us-east-1']

 for region in regions:  

  
  ##############################################################################################################
  ##############################################################################################################
        # # Use STS to assume a temporary role in the sub account that has the Organization service role.
        # # If the sub account does not have the Organization service role it will be excepted.
        try:
            role_arn = ' arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
            sts_response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=sts_role_session_name,
            DurationSeconds=900
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
          break
        else:
          sts_session = session 
        
    ##############################################################################################################
    ##############################################################################################################

        if sts_session != '':

          info = []
        
          #### Code to execute against all regions in every account
          s3_client = sts_session.client('s3', region_name=region)

 # Retrieve the policy of the specified buckets and indicate no policy for buckets without life cycle policy 
          

s3_client = boto3.client('s3')
    
bucket_list = s3_client.list_buckets()

for bucket in bucket_list['Buckets']:

        try:
            lifecycle = s3_client.get_bucket_lifecycle(Bucket=bucket['Name'])
            rules = lifecycle['Rules']
        except:
            rules = 'No Policy'
        print(bucket['Name'], rules)
 

#list the names of the bucket without policy
bucket_list = s3_client.list_buckets()

for bucket in bucket_list['Buckets']:
    bucket_with_no_policy=[]
    try:
        lifecycle = s3_client.get_bucket_lifecycle(Bucket=bucket['Name'])
        rules = lifecycle['Rules']
    except:
        rules = 'No Policy'

    if rules == 'No Policy':
        bucket_with_no_policy.append(bucket['Name'])
        print(bucket_with_no_policy)






lambda_handler(
  {
    'action': 'run'
  },
  'context'
)
            

            


            