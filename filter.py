import boto3
import os
import re
import json
import sys

s3_client = boto3.client('s3')
client = boto3.client('organizations')

regions=[]


# Paginate function
def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result

def lambda_handler(event, context):
  
  role_arn = 'arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
  sts_role_session_name = 'org-session'
  
  session = boto3.Session(region_name='us-east-1')
  org_client = session.client('organizations')
  regions = 'regions'
  #regions = [regions['RegionName'] for regions in session.client('ec2').describe_regions()['Regions']]

  # Get list of ACTIVE accounts in the organization, this list contains only accounts that have been created or accepted
  # an invitation to the organization.  This list will also contain those accounts without the Organization service role.

  org_accounts = []
  for key in paginate(org_client.list_accounts):
    if key['Status'] == 'ACTIVE':
      org_accounts.append(str(key['Id']))

  result = {}
  all_hosts = []

  org = session.client('organizations')

  for account in org_accounts:
    # Iterate through sub accounts
    sts_client = session.client('sts')

    regions = ['us-east-1']

    for region in regions:  

  ##############################################################################################################
  ##############################################################################################################
        # # Use STS to assume a temporary role in the sub account that has the Organization service role.
        # # If the sub account does not have the Organization service role it will be excepted.
        try:
            role_arn = 'arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
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
        # ssm_client = sts_session.client('ssm', region_name=region)
        print('Processing account', account, " and region ", regions)

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
        
#put bucket policy for buckets without life cycle policy

            for bucket in bucket_with_no_policy:
                s3 = boto3.resource('s3')
                bucket_lifecycle_configuration = s3.BucketLifecycleConfiguration(bucket)
                response = bucket_lifecycle_configuration.put(
                    LifecycleConfiguration={
                        'Rules': [
                            {
                                'Expiration': {
                                    'Days': 31,
                                },
                                'ID': 'jcrew-default-s3-lifecycle',
                                'Prefix': '',
                                'Status': 'Enabled',
                                'Transitions': [
                                    {
                                        'Days': 30,
                                        'StorageClass': 'INTELLIGENT_TIERING'
                                    },
                                ],
                                'NoncurrentVersionTransitions': [
                                    {
                                        'NoncurrentDays': 30,
                                        'StorageClass': 'INTELLIGENT_TIERING'
                                    },
                                ],
                                'NoncurrentVersionExpiration': {
                                    'NoncurrentDays': 31
                                },
                                "AbortIncompleteMultipartUpload": {
                                    "DaysAfterInitiation": 7
                                }
                            },
                        ]
                    }
                )




lambda_handler(
  {
    'action': 'run'
  },
  'context'
)
            

            


            




lambda_handler(
  {
    'action': 'run'
  },
  'context'
)
            

            


            