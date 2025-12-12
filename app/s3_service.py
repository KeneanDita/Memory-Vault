import boto3
import os
from botocore.exceptions import ClientError
from config import Config
import uuid
from werkzeug.utils import secure_filename


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=Config.AWS_ENDPOINT_URL,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_DEFAULT_REGION,
        )
        self.bucket_name = Config.S3_BUCKET_NAME

    def upload_file(self, file, content_type, folder="uploads"):
        """Upload a file to S3 and return its URL"""
        try:
            # Generate unique filename
            original_filename = secure_filename(file.filename)
            file_extension = os.path.splitext(original_filename)[1].lower()
            unique_filename = f"{uuid.uuid4()}{file_extension}"

            # Create S3 key
            s3_key = f"{folder}/{unique_filename}"

            # Upload to S3
            self.s3_client.upload_fileobj(
                file, self.bucket_name, s3_key, ExtraArgs={"ContentType": content_type}
            )

            # Generate URL (LocalStack specific)
            file_url = f"{Config.AWS_ENDPOINT_URL}/{self.bucket_name}/{s3_key}"

            return {
                "success": True,
                "s3_key": s3_key,
                "file_url": file_url,
                "original_filename": original_filename,
                "unique_filename": unique_filename,
            }

        except ClientError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_file_url(self, s3_key):
        """Generate a URL for the file"""
        return f"{Config.AWS_ENDPOINT_URL}/{self.bucket_name}/{s3_key}"

    def delete_file(self, s3_key):
        """Delete a file from S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError:
            return False

    def list_files(self, prefix="uploads/"):
        """List all files in the bucket with given prefix"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name, Prefix=prefix
            )

            files = []
            if "Contents" in response:
                for obj in response["Contents"]:
                    files.append(
                        {
                            "key": obj["Key"],
                            "size": obj["Size"],
                            "last_modified": obj["LastModified"],
                            "url": self.get_file_url(obj["Key"]),
                        }
                    )

            return files
        except ClientError as e:
            print(f"Error listing files: {e}")
            return []
