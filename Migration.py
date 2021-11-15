import boto3
import os
import re
import json

import io
# import pytest


ec2=boto3.client("ec2")
ec2_client=boto3.client("ec2")


#@dryable.Dryable ( )
def  get_available_volumes ( results ):
        print [ get_available_volumes ]
 
client = boto3.client('ec2')

regions = 'us-east-1'

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

  # Get list of ACTIVE accounts in the organization, this list contains only accounts that have been created or accepted
  # an invitation to the organization.  This list will also contain those accounts without the Organization service role.

 
  for key in paginate(org_client.list_accounts):
    if key['Status'] == 'ACTIVE':
      org_accounts.append(str(key['Id']))

  result = {}
  all_hosts = []

  org_accounts = ['917848291101']

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
          ec2_client = sts_session.client('ec2', region_name=region)

    
          #print('Processing account', account, " and region ", region)
          try:
            ebs_list = ec2_client.describe_volumes()


            def get_available_volumes():
              '''
              Get all volumes in 'available' state. (Volumes not attached to any instance)
              '''
              for volume in ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])['Volumes']:
                  yield {
                    # 'status': volume['available'],
                    'volumetype': volume['gp2'],
                    'iops': volume['<3000'],
                    'size': volume['<=350']
                }
            print(ebs_list)
          
 
          #   for volume in ebs_list['Volumes']:
          #     if volume['VolumeType'] == 'gp2' or volume['VolumeType'] == 'gp3':
                  
          #         #Assign throughput
          #         if volume['VolumeType'] == 'gp2' and volume['Size'] >= 350:
          #           throughput = 250
          #         else:
          #           throughput = 125

          #         #Assign IOPS
          #         if volume['VolumeType'] == 'gp2' and volume['Iops'] < 3000:
          #           iops = 3000
          #         if volume['VolumeType'] == 'gp2' and volume['Iops'] > 3000:
          #           iops = volume['Iops']
                  
          #         output = account + "," + region + "," + volume['VolumeId'] + "," + volume['VolumeType'] + "," + str(volume['Size']) + "," + str(volume['Iops']) + "," + str(volume.get('Throughput',"NA")) + ",gp3," + str(iops) + "," + str(throughput)
          #         print(output.strip())

          except Exception as e:
            print ('Exception: ', e)

        else:
          print('No valid session') 
          
#dryable.set ( '--dry-run' )

# response = ec2.describe_volumes()
# data = response["Volumes"]
# # print(data[3])
# with io.open("prod.csv","w",encoding="utf-8") as f1:
#     f1.write("status, type, iops, size\n")
#     for volume in data:
        
#         volume_data=volume["Attachments"]
#         if (len(volume_data)>0):
#             status=volume["available"]
#             volumetype=volume["gp2"]
#             iops=volume["<3000"]
#             size=volume["<=350"]
#             # print(device)
#         else:
#             device="not Attached!!"
#             # volumetype="Volumetype not Attached!!"
#         status=volume["available"]
#         size=volume["<=350"]
#         iops=volume["<3000"]
#         type=volume["gp2"]
#         # print(len(data))
#         # print(data[0])
#         f1.write(status+", "+iops+", "+type+", "+str(size)+"\n")

lambda_handler(
  {
    'action': 'run'
  },
  'context'
)