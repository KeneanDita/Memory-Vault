import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "test")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "test")
    AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "memory-vault")

    # DynamoDB Tables
    NOTES_TABLE = os.getenv("NOTES_TABLE", "MemoryVaultNotes")
    IMAGES_TABLE = os.getenv("IMAGES_TABLE", "MemoryVaultImages")
    VIDEOS_TABLE = os.getenv("VIDEOS_TABLE", "MemoryVaultVideos")

    # File upload settings
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    UPLOAD_FOLDER = "/tmp/uploads"
    ALLOWED_EXTENSIONS = {
        "notes": {
            "pdf",
            "txt",
            "doc",
            "docx",
            "ppt",
            "pptx",
            "xls",
            "xlsx",
            "odt",
            "ods",
            "odp",
        },
        "images": {"png", "jpg", "jpeg", "webp", "svg", "gif", "bmp", "tiff"},
        "videos": {"mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "mpeg", "mpg"},
    }
