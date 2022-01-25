import boto3
import os
import re
import json

# Paginate function
def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result

def lambda_handler(event, context):
 
  organization_service_role = 'OrganizationAccountAccessRole'
  sts_role_session_name = 'org-session'
  
  session = boto3.Session(region_name='us-east-1')
  org_client = session.client('organizations')
  regions = [regions['RegionName'] for regions in session.client('ec2').describe_regions()['Regions']]

  # Get list of ACTIVE accounts in the organization, this list contains only accounts that have been created or accepted
  # an invitation to the organization.  This list will also contain those accounts without the Organization service role.

  org_accounts = []
  for key in paginate(org_client.list_accounts):
    if key['Status'] == 'ACTIVE':
      org_accounts.append(str(key['Id']))

  ### Debug Overides ###
  #org_accounts = ['917848291101']
  regions = ['us-east-1','us-west-2']

  for account in org_accounts:
    # Iterate through sub accounts
    sts_client = session.client('sts')

    #regions = ['us-east-1','us-west-2']

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

          info = []
        
          #### Code to execute against all regions in every account
          s3_client = sts_session.client('s3', region_name=region)
          
      
          
          s3_list = s3_client.list_buckets()

          for bucket in s3_list['Buckets']:

              print(account, " - ", region, " - ", bucket['Name'])
            
              try:
                tags = s3_client.get_bucket_tagging(
                      Bucket=bucket['Name'],
                  )
              except Exception as e:
                if "(NoSuchTagSet)" in str(e):
                  print ('Puting tags')                  s3_client.put_bucket_tagging(
                    Bucket=bucket['Name'],
                    Tagging={'TagSet': 
                      [
                        {
                          'Key': 'map-migrated',
                          'Value': 'd-server-01t0vi3wnnt294'
                        },
                        {
                          'Key': 'S3-Bucket-Name',
                         'Value': bucket['Name']
                        }
                      ]
                    },
                  )
                else:
                  print ('Exception: ', e)
        #         continue
              
        #       s3_found = 0
        #       map_found = 0 

        #       for tag in tags['TagSet']:

        #         if tag['Key'] == 'S3-Bucket-Name':
        #           s3_found = 1

        #         if tag['Key'] == 'map-migrated':
        #           map_found = 1

        #       if s3_found == 0:
        #         tags['TagSet'].append({'Key':'S3-Bucket-Name', 'Value': bucket['Name']})
        #       else:
        #         tag['Value'] = (bucket['Name'])

        #       if map_found == 0:
        #         tags['TagSet'].append({'Key':'map-migrated', 'Value': 'd-server-01t0vi3wnnt294'})
        #       else:
        #         tag['Value'] = 'd-server-01t0vi3wnnt294'

        #       s3_client.put_bucket_tagging(
        #           Bucket=bucket['Name'],
        #           Tagging={'TagSet': tags['TagSet']},
        #       )

        #   except Exception as e:
        #     print ('Exception: ', e)
        #     continue

        # else:
        #   print('No valid session')  

lambda_handler(
  {
    'action': 'run'
  },
  'context'
)