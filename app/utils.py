import os
from PIL import Image
import filetype
from config import Config


def allowed_file(filename, file_type):
    """Check if the file extension is allowed"""
    if "." not in filename:
        return False

    ext = filename.rsplit(".", 1)[1].lower()
    return ext in Config.ALLOWED_EXTENSIONS.get(file_type, set())


def get_file_type(filename):
    """Determine file type based on extension"""
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else ""

    if ext in Config.ALLOWED_EXTENSIONS["notes"]:
        return "notes"
    elif ext in Config.ALLOWED_EXTENSIONS["images"]:
        return "images"
    elif ext in Config.ALLOWED_EXTENSIONS["videos"]:
        return "videos"
    return "unknown"


def get_mime_type(file_path):
    """Get MIME type of file using filetype library"""
    try:
        kind = filetype.guess(file_path)
        if kind is not None:
            return kind.mime
        else:
            # Fallback based on extension
            ext = os.path.splitext(file_path)[1].lower()
            mime_map = {
                ".pdf": "application/pdf",
                ".txt": "text/plain",
                ".doc": "application/msword",
                ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                ".ppt": "application/vnd.ms-powerpoint",
                ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                ".xls": "application/vnd.ms-excel",
                ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp",
                ".svg": "image/svg+xml",
                ".mp4": "video/mp4",
                ".mkv": "video/x-matroska",
                ".avi": "video/x-msvideo",
                ".mov": "video/quicktime",
                ".wmv": "video/x-ms-wmv",
                ".flv": "video/x-flv",
                ".webm": "video/webm",
            }
            return mime_map.get(ext, "application/octet-stream")
    except:
        return "application/octet-stream"


def get_image_dimensions(file_path):
    """Get image dimensions"""
    try:
        with Image.open(file_path) as img:
            return {"width": img.width, "height": img.height}
    except:
        return {"width": 0, "height": 0}


def format_file_size(size):
    """Format file size to human readable format"""
    if size == 0:
        return "0 B"

    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"


def validate_file_mime_type(file_path, expected_type):
    """
    Validate that the file's actual MIME type matches expected type
    expected_type: 'notes', 'images', or 'videos'
    """
    mime_type = get_mime_type(file_path)

    if expected_type == "notes":
        # Document MIME types
        document_mimes = [
            "application/pdf",
            "text/plain",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/vnd.ms-powerpoint",
            "application/vnd.openxmlformats-officedocument.presentationml.presentation",
            "application/vnd.ms-excel",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "application/vnd.oasis.opendocument.text",
            "application/vnd.oasis.opendocument.spreadsheet",
            "application/vnd.oasis.opendocument.presentation",
        ]
        return mime_type in document_mimes

    elif expected_type == "images":
        # Image MIME types
        image_mimes = [
            "image/jpeg",
            "image/png",
            "image/gif",
            "image/webp",
            "image/svg+xml",
            "image/bmp",
            "image/tiff",
        ]
        return mime_type.startswith("image/") or mime_type in image_mimes

    elif expected_type == "videos":
        # Video MIME types
        video_mimes = [
            "video/mp4",
            "video/x-matroska",
            "video/x-msvideo",
            "video/quicktime",
            "video/x-ms-wmv",
            "video/x-flv",
            "video/webm",
            "video/mpeg",
        ]
        return mime_type.startswith("video/") or mime_type in video_mimes

    return False
