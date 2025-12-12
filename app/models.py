from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal  # Add this import
import json


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)


@dataclass
class BaseFile:
    """Base model for all file types"""

    title: Optional[str] = None
    description: Optional[str] = None
    s3_key: str = ""
    file_url: str = ""
    original_filename: str = ""
    file_type: str = ""
    file_size: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        data = asdict(self)
        data["created_at"] = self.created_at
        data["updated_at"] = self.updated_at
        return data

    def to_json(self) -> str:
        """Convert model to JSON string"""
        return json.dumps(self.to_dict(), cls=DecimalEncoder)


@dataclass
class Note(BaseFile):
    """Model for notes/documents"""

    note_id: str = ""
    tags: Optional[list] = None

    def __post_init__(self):
        super().__post_init__()
        if self.tags is None:
            self.tags = []


@dataclass
class Image(BaseFile):
    """Model for images"""

    image_id: str = ""
    dimensions: Optional[Dict[str, int]] = None
    exif_data: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        super().__post_init__()
        if self.dimensions is None:
            self.dimensions = {"width": 0, "height": 0}


@dataclass
class Video(BaseFile):
    """Model for videos"""

    video_id: str = ""
    duration: float = 0.0
    resolution: Optional[str] = None
    thumbnail_key: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()


# Factory functions for creating models from DynamoDB items
def create_note_from_dict(data: Dict[str, Any]) -> Note:
    """Create Note object from DynamoDB item"""
    # Convert Decimal values to float
    converted_data = {}
    for key, value in data.items():
        if isinstance(value, Decimal):
            converted_data[key] = float(value)
        elif isinstance(value, dict):
            # Recursively convert nested dicts
            converted_data[key] = {
                k: float(v) if isinstance(v, Decimal) else v for k, v in value.items()
            }
        else:
            converted_data[key] = value

    return Note(
        note_id=converted_data.get("note_id", ""),
        title=converted_data.get("title"),
        description=converted_data.get("description"),
        s3_key=converted_data.get("s3_key", ""),
        file_url=converted_data.get("file_url", ""),
        original_filename=converted_data.get("original_filename", ""),
        file_type=converted_data.get("file_type", ""),
        file_size=converted_data.get("file_size", 0),
        created_at=converted_data.get("created_at"),
        updated_at=converted_data.get("updated_at"),
        tags=converted_data.get("tags", []),
    )


def create_image_from_dict(data: Dict[str, Any]) -> Image:
    """Create Image object from DynamoDB item"""
    # Convert Decimal values to float
    converted_data = {}
    for key, value in data.items():
        if isinstance(value, Decimal):
            converted_data[key] = float(value)
        elif isinstance(value, dict):
            converted_data[key] = {
                k: float(v) if isinstance(v, Decimal) else v for k, v in value.items()
            }
        else:
            converted_data[key] = value

    return Image(
        image_id=converted_data.get("image_id", ""),
        title=converted_data.get("title"),
        description=converted_data.get("description"),
        s3_key=converted_data.get("s3_key", ""),
        file_url=converted_data.get("file_url", ""),
        original_filename=converted_data.get("original_filename", ""),
        file_type=converted_data.get("file_type", ""),
        file_size=converted_data.get("file_size", 0),
        created_at=converted_data.get("created_at"),
        updated_at=converted_data.get("updated_at"),
        dimensions=converted_data.get("dimensions", {}),
        exif_data=converted_data.get("exif_data", {}),
    )


def create_video_from_dict(data: Dict[str, Any]) -> Video:
    """Create Video object from DynamoDB item"""
    # Convert Decimal values to float
    converted_data = {}
    for key, value in data.items():
        if isinstance(value, Decimal):
            converted_data[key] = float(value)
        elif isinstance(value, dict):
            converted_data[key] = {
                k: float(v) if isinstance(v, Decimal) else v for k, v in value.items()
            }
        else:
            converted_data[key] = value

    return Video(
        video_id=converted_data.get("video_id", ""),
        title=converted_data.get("title"),
        description=converted_data.get("description"),
        s3_key=converted_data.get("s3_key", ""),
        file_url=converted_data.get("file_url", ""),
        original_filename=converted_data.get("original_filename", ""),
        file_type=converted_data.get("file_type", ""),
        file_size=converted_data.get("file_size", 0),
        created_at=converted_data.get("created_at"),
        updated_at=converted_data.get("updated_at"),
        duration=converted_data.get("duration", 0.0),
        resolution=converted_data.get("resolution"),
        thumbnail_key=converted_data.get("thumbnail_key"),
    )
