
import boto3
from botocore.exceptions import ClientError

from datetime import datetime,timedelta

def delete_snapshot(snapshot_id, reg):
    try:
        ec2resource = boto3.resource('ec2', region_name=reg)
        snapshot = ec2resource.Snapshot(snapshot_id)
        snapshot.delete()
    except ClientError as e:
        print ("Caught exception: %s" % e)

    return

def lambda_handler(event, context):
account_id = '335418536307'
retention_days = 1
    # Get current timestamp in UTC
now = datetime.now()

    # AWS Account ID

    # Define retention period in days

    # Create EC2 client
ec2 = boto3.client('ec2')
    
   
def lambda_handler(event, context):
 
  organization_service_role = 'OrganizationAccountAccessRole'
  sts_role_session_name = 'org-session'
  
  session = boto3.Session(region_name='us-east-1')
  org_client = session.client('organizations') 

    # Get list of regions
  regions = ec2.describe_regions().get('Regions',[] )
    
    

  org_accounts = []
  for key in paginate(org_client.list_accounts):
    if key['Status'] == 'ACTIVE':
      org_accounts.append(str(key['Id']))

  result = {}
  all_hosts = []

  # org_accounts = ['335418536307']

  for account in org_accounts:
    # if account in ["513936039192", "345625197086", "513057034381", "335418536307"]:
    #   print('Cannot assume role for account {}'.format(account))
    # else:
      # Iterate through sub accounts
      sts_client = session.client('sts')

      #regions = ['us-east-1']
      regions = ['us-east-1','us-west-2']

      for region in regions:  
       
       print('=========================================================================================================================================')
       print('Processing account', account and 'region ', region)

    ##############################################################################################################
    ##############################################################################################################
          # # Use STS to assume a temporary role in the sub account that has the Organization service role.
          # # If the sub account does not have the Organization service role it will be excepted.
       try:
          role_arn = 'arn:aws:iam::' + account + ':role/' + organization_service_role
          # role_arn = 'arn:aws:iam::335418536307:role/aws-reserved/sso.amazonaws.com/AWSReservedSSO_account-admin_788ae45a0b3e7ff0'
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
          
    # Iterate over regions
    for region in regions:
       

        # Connect to region
        ec2 = boto3.client('ec2', region_name=reg)

        # Filtering by snapshot timestamp comparison is not supported
        # So we grab all snapshot id's
        result = ec2.describe_snapshots( OwnerIds=[account_id] )

        for snapshot in result['Snapshots']:
            print ("Checking snapshot %s which was created on %s" )% (snapshot['SnapshotId'],snapshot['StartTime'])

            # Remove timezone info from snapshot in order for comparison to work below
            snapshot_time = snapshot['StartTime'].replace(tzinfo=None)

            # Subtract snapshot time from now returns a timedelta
            # Check if the timedelta is greater than retention days
            if (now - snapshot_time) > timedelta(retention_days):
                print( "Snapshot is older than configured retention of %d days" )% (retention_days)
                delete_snapshot(snapshot['SnapshotId'], reg)
            else:
                print ("Snapshot is newer than configured retention of %d days so we keep it") % (retention_days)