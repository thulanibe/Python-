import boto3
import json
import os

# Paginate function
def paginate(method, **kwargs):
    client = method.__self__
    paginator = client.get_paginator(method.__name__)
    for page in paginator.paginate(**kwargs).result_key_iters():
        for result in page:
            yield result

# Main entry point for the Lambda Function.
def lambda_handler(event, context):
# Set environment variables
  aws_region = os.environ.get('aws_region')
  function_name = os.environ.get('function_name')
  accounts_to_exclude = os.environ.get('accounts_to_exclude')
  organization_service_role = os.environ.get('organization_service_role')
  sts_role_session_name = os.environ.get('sts_role_session_name')
  session = boto3.Session(region_name=aws_region)
  org_session = session.client('organizations')
  master_accountId = org_session.describe_organization()['Organization']['MasterAccountId']
  sts_client = session.client('sts')
  print(str(event))
  if 'CodePipeline.job' in event:
    job_id = event['CodePipeline.job']['id']
    code_pipeline = session.client('codepipeline')

  # Get list of ACTIVE accounts in the organization, this list contains only accounts that have been created or accepted
  # an invitation to the organization.  This list will also contain those accounts without the Organization service role.
  org_response = org_session.list_accounts()
  org_accounts = []
  for key in paginate(org_session.list_accounts):
    if key['Status'] == 'ACTIVE':
      org_accounts.append(str(key['Id']))

  accounts_to_exclude = [account for account in accounts_to_exclude.split(',')]
  org_accounts = list(set(org_accounts) - set(accounts_to_exclude))
  print('Excluding accounts', list(set(accounts_to_exclude)))
  print('processing accounts', org_accounts)

  #Use the variable below to 
  org_accounts = [917848291101]

  # Execute CloudWatch Lambda task function
  lambda_client = session.client('lambda')
  for account in org_accounts:
    if account not in accounts_to_exclude:
      try:
        if account != master_accountId:
          role_arn = 'arn:aws:iam::' + account + ':role/' + organization_service_role
          sts_response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=sts_role_session_name,
            DurationSeconds=900
            )
        
        print('Calling Lambda function to process account ', account)
        payload = {
          "account": account
        }
        payload = json.dumps(payload)
        print(payload)
        lambda_client.invoke(
          FunctionName=function_name,
          InvocationType='Event',
          LogType='Tail',
          Payload=payload
          )
      except Exception as err:
        # If sub account does not have Organization service role we log it and ignore the account.
        print('failed to assume role for account', account, err)
      if 'CodePipeline.job' in event:
        code_pipeline.put_job_success_result(jobId=job_id)




# Feedback
# English (US)
