import json
import boto3
BUCKET_NAME='gfgbucket'
def create_bucket_policy():
	bucket_policy = {
		"Version": "2012-10-17",
		"Statement": [
			{
				"Sid": "AddPerm",
				"Effect": "Allow",
				"Principal": "*",
				"Action": ["s3:*"],
				"Resource": ["arn:aws:s3:::gfgbucket/*"]
			}
		]
	}

	policy_string = json.dumps(bucket_policy)

	s3_client().put_bucket_policy(
		Bucket=BUCKET_NAME,
		Policy=policy_string
	)
