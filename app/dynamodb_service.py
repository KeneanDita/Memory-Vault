import boto3
from boto3.dynamodb.conditions import Key
from config import Config
import uuid
from datetime import datetime
from decimal import Decimal
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)


class DynamoDBService:
    def __init__(self):
        self.dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=Config.AWS_ENDPOINT_URL,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_DEFAULT_REGION,
        )

        self.notes_table = self.dynamodb.Table(Config.NOTES_TABLE)
        self.images_table = self.dynamodb.Table(Config.IMAGES_TABLE)
        self.videos_table = self.dynamodb.Table(Config.VIDEOS_TABLE)

    def create_note(self, data):
        """Create a new note record"""
        note_id = str(uuid.uuid4())
        item = {
            "note_id": note_id,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "s3_key": data["s3_key"],
            "file_url": data["file_url"],
            "original_filename": data["original_filename"],
            "file_type": data.get("file_type", ""),
            "file_size": data.get("file_size", 0),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self.notes_table.put_item(Item=item)
        return note_id

    def create_image(self, data):
        """Create a new image record"""
        image_id = str(uuid.uuid4())
        item = {
            "image_id": image_id,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "s3_key": data["s3_key"],
            "file_url": data["file_url"],
            "original_filename": data["original_filename"],
            "file_type": data.get("file_type", ""),
            "file_size": data.get("file_size", 0),
            "dimensions": data.get("dimensions", {}),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self.images_table.put_item(Item=item)
        return image_id

    def create_video(self, data):
        """Create a new video record"""
        video_id = str(uuid.uuid4())
        item = {
            "video_id": video_id,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "s3_key": data["s3_key"],
            "file_url": data["file_url"],
            "original_filename": data["original_filename"],
            "file_type": data.get("file_type", ""),
            "file_size": data.get("file_size", 0),
            "duration": data.get("duration", 0),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }

        self.videos_table.put_item(Item=item)
        return video_id

    def get_all_notes(self):
        """Get all notes"""
        response = self.notes_table.scan()
        return response.get("Items", [])

    def get_all_images(self):
        """Get all images"""
        response = self.images_table.scan()
        return response.get("Items", [])

    def get_all_videos(self):
        """Get all videos"""
        response = self.videos_table.scan()
        return response.get("Items", [])

    def get_note_by_id(self, note_id):
        """Get a specific note by ID"""
        response = self.notes_table.get_item(Key={"note_id": note_id})
        return response.get("Item")

    def get_image_by_id(self, image_id):
        """Get a specific image by ID"""
        response = self.images_table.get_item(Key={"image_id": image_id})
        return response.get("Item")

    def get_video_by_id(self, video_id):
        """Get a specific video by ID"""
        response = self.videos_table.get_item(Key={"video_id": video_id})
        return response.get("Item")

    def delete_note(self, note_id):
        """Delete a note by ID"""
        self.notes_table.delete_item(Key={"note_id": note_id})

    def delete_image(self, image_id):
        """Delete an image by ID"""
        self.images_table.delete_item(Key={"image_id": image_id})

    def delete_video(self, video_id):
        """Delete a video by ID"""
        self.videos_table.delete_item(Key={"video_id": video_id})

    def search_items(self, table_name, search_term):
        """Search items by title or description"""
        table_map = {
            "notes": self.notes_table,
            "images": self.images_table,
            "videos": self.videos_table,
        }

        table = table_map.get(table_name)
        if not table:
            return []

        # Scan is simple but not efficient for large datasets
        # In production, consider using ElasticSearch or DynamoDB streams
        response = table.scan()
        items = response.get("Items", [])

        if search_term:
            search_term = search_term.lower()
            filtered_items = []
            for item in items:
                title = item.get("title", "").lower()
                description = item.get("description", "").lower()
                if search_term in title or search_term in description:
                    filtered_items.append(item)
            return filtered_items

        return items
