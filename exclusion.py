
import boto3
from botocore.exceptions import ClientError


def get_bucket_lifecycle_of_s3(bucket_name):
   session = boto3.session.Session()
   s3_client = session.client('s3')
   try:
      results = s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name,)
   except ClientError as e:
      raise Exception( "boto3 client error in get_bucket_lifecycle_of_s3 function: " + e.__str__())
   except Exception as e:
      raise Exception( "Unexpected error in get_bucket_lifecycle_of_s3 function: " + e.__str__())
      return results

print(get_bucket_lifecycle_of_s3("Bucket_name"))