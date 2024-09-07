from datetime import datetime
import logging
import boto3
from botocore.exceptions import ClientError

class S3Client:

    def __init__(self, s3_bucket_name: str, aws_access_key_id: str, aws_secret_access_key: str, aws_region_name: str):
        self.s3_bucket_name = s3_bucket_name
        self.aws_region_name = aws_region_name
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region_name
        )

    def upload_screenshot(self, screenshot_as_bytes: bytes, step_name: str) -> str:
        key = f"screenshots/{step_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        try:
            self.client.put_object(
                Bucket=self.s3_bucket_name,
                Key=key,
                Body=screenshot_as_bytes,
                ContentType='image/png',
                ACL='public-read'
            )
            print(f"Uploaded screenshot to s3://{self.s3_bucket_name}/{key}")
        except ClientError as error:
            logging.error(f"Failed to upload screenshot to S3: {error}")
            raise Exception(f"Could not upload the screenshot: {error}")

        file_url = f'https://{self.s3_bucket_name}.s3.{self.aws_region_name}.amazonaws.com/{key}'
        return file_url