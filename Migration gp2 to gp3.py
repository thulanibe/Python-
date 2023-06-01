import boto3

def migrate_volumes(event, context):
    # Get the list of AWS accounts
    organizations_client = boto3.client('organizations')
    accounts = organizations_client.list_accounts()['Accounts']

    # Iterate over each AWS account
    for account in accounts:
        account_id = account['Id']
        print(f"Migrating volumes in Account: {account_id}")

        # Assume role in the account
        sts_client = boto3.client('sts')
        role_arn = f"arn:aws:iam::{account_id}:role/YourAssumedRole"
        assumed_role = sts_client.assume_role(RoleArn=role_arn, RoleSessionName="AssumeRoleSession")

        # Switch to the assumed role's credentials
        session = boto3.Session(
            aws_access_key_id=assumed_role['Credentials']['AccessKeyId'],
            aws_secret_access_key=assumed_role['Credentials']['SecretAccessKey'],
            aws_session_token=assumed_role['Credentials']['SessionToken']
        )

        # Get the list of regions
        ec2_client = session.client('ec2')
        regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

        # Iterate over each region in the account
        for region in regions:
            print(f"Migrating volumes in Region: {region}")

            # Get the list of volumes in the region
            ec2_resource = session.resource('ec2', region_name=region)
            volumes = ec2_resource.volumes.filter(Filters=[{'Name': 'volume-type', 'Values': ['gp2']}])

            # Migrate each gp2 volume to gp3
            for volume in volumes:
                volume.modify_attribute(VolumeType={'Value': 'gp3'})

    return {
        'statusCode': 200,
        'body': 'Volume migration completed.'
    }
