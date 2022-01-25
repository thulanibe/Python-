import boto3
import os
import re
import json
import sys


client = boto3.client('s3')
client = boto3.client('organizations')


# Paginate function
def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result
            

def lambda_handler(event, context):
  
  
  role_arn = 'arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
  #organization_service_role = 'OrganizationAccountAccessRole1'
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

  #org_accounts = ["335418536307"]

  for account in org_accounts:
    # Iterate through sub accounts
    sts_client = session.client('sts')

    regions = ['us-east-1','us-west-2']

    for region in regions:  


  ##############################################################################################################
  ##############################################################################################################
        # # Use STS to assume a temporary role in the sub account that has the Organization service role.
        # # If the sub account does not have the Organization service role it will be excepted.
        try:
            role_arn = 'arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
            #role_arn = 'arn:aws:iam::' + account + ':role/' + organization_service_role
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

          print('Processing account', account, " and region ", region)
        
           #put lifecycle policy if there's no policy                  
                
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
                        
                
                
            
                
                
                
                
        except Exception as e:
            print('Exception: ', e)
            
   
  result['all'] = all_hosts  
            
        



lambda_handler(
    {
         'action': 'run'
    },
    'context'
    )          