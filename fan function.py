import boto3

def fan_function_across_regions_accounts():
    # Create a session with your AWS credentials
    session = boto3.Session()

    # Iterate over all available regions
    for region in session.get_available_regions('ec2'):
        # Create a new EC2 client for the region
        ec2_client = session.client('ec2', region_name=region)

        # Retrieve a list of all accounts in the AWS Organization
        org_client = session.client('organizations')
        accounts = org_client.list_accounts()

        # Iterate over all accounts
        for account in accounts['Accounts']:
            # Assume a role in the account to perform actions
            sts_client = session.client('sts')
            assumed_role = sts_client.assume_role(
                RoleArn=account['Arn'],
                RoleSessionName='AssumedRoleSession'
            )
            assumed_credentials = assumed_role['Credentials']

            # Create a new EC2 client in the account with assumed credentials
            account_ec2_client = boto3.client(
                'ec2',
                region_name=region,
                aws_access_key_id=assumed_credentials['AccessKeyId'],
                aws_secret_access_key=assumed_credentials['SecretAccessKey'],
                aws_session_token=assumed_credentials['SessionToken']
            )

            # Perform actions using the account's EC2 client
            # ...
            # Implement your desired logic here

            # Example: Print the instances in the account's region
            response = account_ec2_client.describe_instances()
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    print(f"Account: {account['Id']}, Region: {region}, InstanceId: {instance['InstanceId']}")

# Call the function
fan_function_across_regions_accounts()
