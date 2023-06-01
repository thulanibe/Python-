import boto3

def lambda_handler(event, context):
    # Get a list of all AWS accounts in the organization
    org_client = boto3.client('organizations')
    accounts = org_client.list_accounts()['Accounts']
    
    for account in accounts:
        # Assume a role in each account
        sts_client = boto3.client('sts')
        assumed_role = sts_client.assume_role(
            RoleArn='arn:aws:iam::' + account['Id'] + ':role/YourRoleName',
            RoleSessionName='VPCFlowsCheck'
        )
        credentials = assumed_role['Credentials']
        
        # Get the list of regions for each account
        ec2_client = boto3.client('ec2', region_name='us-east-1', 
                                  aws_access_key_id=credentials['AccessKeyId'],
                                  aws_secret_access_key=credentials['SecretAccessKey'],
                                  aws_session_token=credentials['SessionToken'])
        regions = ec2_client.describe_regions()['Regions']
        
        for region in regions:
            region_name = region['RegionName']
            vpc_client = boto3.client('ec2', region_name=region_name, 
                                      aws_access_key_id=credentials['AccessKeyId'],
                                      aws_secret_access_key=credentials['SecretAccessKey'],
                                      aws_session_token=credentials['SessionToken'])
            
            # Retrieve VPC peering connections in the region
            peering_connections = vpc_client.describe_vpc_peering_connections()['VpcPeeringConnections']
            
            # Check the VPC flows for each peering connection
            for connection in peering_connections:
                # Check if the VPC flow logs are enabled or disabled for the connection
                vpc_flows_enabled = connection.get('RequesterVpcInfo', {}).get('VpcFlowLogs', [])
                
                if vpc_flows_enabled:
                    print(f"VPC flows are enabled for peering connection {connection['VpcPeeringConnectionId']} in account {account['Id']} ({account['Name']}) in region {region_name}.")
                else:
                    print(f"VPC flows are not enabled for peering connection {connection['VpcPeeringConnectionId']} in account {account['Id']} ({account['Name']}) in region {region_name}.")
