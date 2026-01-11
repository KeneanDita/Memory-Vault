from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    send_file,
)
from app.s3_service import S3Service
from app.dynamodb_service import DynamoDBService
from app.models import (
    create_note_from_dict,
    create_image_from_dict,
    create_video_from_dict,
)
from app.utils import (
    allowed_file,
    get_file_type,
    get_mime_type,
    get_image_dimensions,
    format_file_size,
    validate_file_mime_type,
)
import os
from config import Config
import tempfile
from datetime import datetime

bp = Blueprint("main", __name__)
s3_service = S3Service()
db_service = DynamoDBService()


@bp.route("/")
def index():
    """Home page with upload and browse options"""
    # Get counts for display
    notes = db_service.get_all_notes()
    images = db_service.get_all_images()
    videos = db_service.get_all_videos()

    # Convert to models
    note_models = [create_note_from_dict(note) for note in notes]
    image_models = [create_image_from_dict(image) for image in images]
    video_models = [create_video_from_dict(video) for video in videos]

    # Get all files combined and sort by date
    all_files = note_models + image_models + video_models
    # Sort by created_at (newest first)
    all_files.sort(
        key=lambda x: x.created_at if hasattr(x, "created_at") else "", reverse=True
    )

    # Take only recent 5 files
    recent_files = all_files[:5]

    # Format file sizes
    for file in recent_files:
        if hasattr(file, "file_size"):
            file.formatted_size = format_file_size(file.file_size)

    return render_template(
        "index.html",
        notes_count=len(note_models),
        images_count=len(image_models),
        videos_count=len(video_models),
        recent_files=recent_files,  # Add this
    )


@bp.route("/stats")
def statistics():
    """Show statistics about stored files"""
    notes = db_service.get_all_notes()
    images = db_service.get_all_images()
    videos = db_service.get_all_videos()

    # Calculate statistics
    notes_count = len(notes)
    images_count = len(images)
    videos_count = len(videos)
    total_count = notes_count + images_count + videos_count

    # Calculate total size
    notes_size = sum(note.get("file_size", 0) for note in notes)
    images_size = sum(image.get("file_size", 0) for image in images)
    videos_size = sum(video.get("file_size", 0) for video in videos)
    total_size = notes_size + images_size + videos_size

    # Format sizes
    notes_size_fmt = format_file_size(notes_size)
    images_size_fmt = format_file_size(images_size)
    videos_size_fmt = format_file_size(videos_size)
    total_size_fmt = format_file_size(total_size)

    # Get recent files for activity
    all_files = []
    for note in notes:
        note_dict = create_note_from_dict(note)
        note_dict.formatted_size = format_file_size(note.get("file_size", 0))
        all_files.append(note_dict)

    for image in images:
        image_dict = create_image_from_dict(image)
        image_dict.formatted_size = format_file_size(image.get("file_size", 0))
        all_files.append(image_dict)

    for video in videos:
        video_dict = create_video_from_dict(video)
        video_dict.formatted_size = format_file_size(video.get("file_size", 0))
        all_files.append(video_dict)

    # Sort by created_at (newest first)
    all_files.sort(
        key=lambda x: x.created_at if hasattr(x, "created_at") else "", reverse=True
    )
    recent_files = all_files[:10]

    return render_template(
        "stats.html",
        notes_count=notes_count,
        images_count=images_count,
        videos_count=videos_count,
        total_count=total_count,
        notes_size=notes_size_fmt,
        images_size=images_size_fmt,
        videos_size=videos_size_fmt,
        total_size=total_size_fmt,
        recent_files=recent_files,  # Add this
        usage_percentage=min(
            100, (total_size / (1024 * 1024 * 1024)) * 100
        ),  # Calculate as % of 1GB
    )


@bp.route("/upload", methods=["GET", "POST"])
def upload():
    """Upload page with tabs for different file types"""
    if request.method == "POST":
        file_type = request.form.get("file_type")
        title = request.form.get("title", "")
        description = request.form.get("description", "")

        if "file" not in request.files:
            flash("No file selected", "error")
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            flash("No file selected", "error")
            return redirect(request.url)

        if not allowed_file(file.filename, file_type):
            flash("File type not allowed", "error")
            return redirect(request.url)

        # Create a unique temporary file name
        import tempfile
        import shutil

        tmp_path = None
        try:
            # Save to a temporary file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=os.path.splitext(file.filename)[1]
            ) as tmp_file:
                tmp_path = tmp_file.name
                file.save(tmp_path)

            # Validate actual file type
            if not validate_file_mime_type(tmp_path, file_type):
                flash(f"File content doesn't match expected type: {file_type}", "error")
                if tmp_path and os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                return redirect(request.url)

            # Get file metadata
            file_size = os.path.getsize(tmp_path)
            mime_type = get_mime_type(tmp_path)

            # Upload to S3 - read from the saved file
            with open(tmp_path, "rb") as file_obj:
                upload_result = s3_service.upload_file(
                    file_obj,
                    mime_type,
                    folder=file_type,
                    original_filename=file.filename,
                )

            if upload_result["success"]:
                # Prepare metadata for DynamoDB
                metadata = {
                    "title": title,
                    "description": description,
                    "s3_key": upload_result["s3_key"],
                    "file_url": upload_result["file_url"],
                    "original_filename": upload_result["original_filename"],
                    "file_type": mime_type,
                    "file_size": file_size,
                }

                # Store metadata in appropriate table
                if file_type == "notes":
                    note_id = db_service.create_note(metadata)
                    flash(
                        f"Note '{upload_result['original_filename']}' uploaded successfully!",
                        "success",
                    )
                elif file_type == "images":
                    # Get image dimensions
                    metadata["dimensions"] = get_image_dimensions(tmp_path)
                    image_id = db_service.create_image(metadata)
                    flash(
                        f"Image '{upload_result['original_filename']}' uploaded successfully!",
                        "success",
                    )
                elif file_type == "videos":
                    metadata["duration"] = 0  # Placeholder for video duration
                    video_id = db_service.create_video(metadata)
                    flash(
                        f"Video '{upload_result['original_filename']}' uploaded successfully!",
                        "success",
                    )

            else:
                flash(f"Upload failed: {upload_result['error']}", "error")

        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            import traceback

            print(f"Upload error: {traceback.format_exc()}")
        finally:
            # Cleanup temp file with retry logic for Windows
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except PermissionError:
                    # Windows might still have the file locked, try again after a delay
                    import time

                    time.sleep(0.1)
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass  # Give up if still locked

        return redirect(url_for("main.browse"))

    # GET request - show upload form
    file_type = request.args.get("type", "notes")
    return render_template("upload.html", current_type=file_type)


@bp.route("/browse")
def browse():
    """Browse all stored files with tabs"""
    tab = request.args.get("tab", "notes")
    search_term = request.args.get("search", "")
    sort_by = request.args.get("sort", "newest")  # Get sort parameter
    sort_order = request.args.get("order", "desc")  # Get order parameter

    # Get items based on tab and convert to models
    if tab == "notes":
        if search_term:
            items_data = db_service.search_items("notes", search_term)
        else:
            items_data = db_service.get_all_notes()
        items = [create_note_from_dict(item) for item in items_data]
        file_type = "notes"
    elif tab == "images":
        if search_term:
            items_data = db_service.search_items("images", search_term)
        else:
            items_data = db_service.get_all_images()
        items = [create_image_from_dict(item) for item in items_data]
        file_type = "images"
    elif tab == "videos":
        if search_term:
            items_data = db_service.search_items("videos", search_term)
        else:
            items_data = db_service.get_all_videos()
        items = [create_video_from_dict(item) for item in items_data]
        file_type = "videos"
    else:
        items = []
        file_type = "notes"

    # Apply sorting
    items = sort_files(items, sort_by, sort_order)

    # Format file sizes and prepare for template
    for item in items:
        if hasattr(item, "file_size"):
            item.formatted_size = format_file_size(item.file_size)

    # Get counts for all tabs
    all_notes = db_service.get_all_notes()
    all_images = db_service.get_all_images()
    all_videos = db_service.get_all_videos()

    # Calculate total_count
    total_count = len(all_notes) + len(all_images) + len(all_videos)

    return render_template(
        "browse.html",
        items=items,
        current_tab=tab,
        search_term=search_term,
        file_type=file_type,
        notes_count=len(all_notes),
        images_count=len(all_images),
        videos_count=len(all_videos),
        total_count=total_count,
        sort_by=sort_by,
        sort_order=sort_order,
    )


def sort_files(files, sort_by="newest", order="desc"):
    """Sort files based on criteria"""
    if not files:
        return files

    # Determine sort key
    if sort_by == "name":
        sort_key = lambda x: (x.title or x.original_filename or "").lower()
    elif sort_by == "size":
        sort_key = lambda x: getattr(x, "file_size", 0)
    elif sort_by == "type":
        sort_key = lambda x: getattr(x, "file_type", "")
    else:  # Default to date (newest/oldest)
        sort_key = lambda x: getattr(x, "created_at", "")

    # Sort the files
    sorted_files = sorted(files, key=sort_key, reverse=(order == "desc"))

    return sorted_files


@bp.route("/view/<file_type>/<item_id>")
def view_item(file_type, item_id):
    """View specific item details"""
    if file_type == "note":
        item_data = db_service.get_note_by_id(item_id)
        if item_data:
            item = create_note_from_dict(item_data)
    elif file_type == "image":
        item_data = db_service.get_image_by_id(item_id)
        if item_data:
            item = create_image_from_dict(item_data)
    elif file_type == "video":
        item_data = db_service.get_video_by_id(item_id)
        if item_data:
            item = create_video_from_dict(item_data)
    else:
        item = None

    if not item:
        flash("Item not found", "error")
        return redirect(url_for("main.browse"))

    # Format file size
    if hasattr(item, "file_size"):
        item.formatted_size = format_file_size(item.file_size)

    return render_template("view_content.html", item=item, file_type=file_type)


@bp.route("/delete/<file_type>/<item_id>", methods=["POST"])
def delete_item(file_type, item_id):
    """Delete an item"""
    # Get item first to get S3 key
    if file_type == "note":
        item = db_service.get_note_by_id(item_id)
        if item:
            s3_service.delete_file(item["s3_key"])
            db_service.delete_note(item_id)
            flash("Note deleted successfully", "success")
    elif file_type == "image":
        item = db_service.get_image_by_id(item_id)
        if item:
            s3_service.delete_file(item["s3_key"])
            db_service.delete_image(item_id)
            flash("Image deleted successfully", "success")
    elif file_type == "video":
        item = db_service.get_video_by_id(item_id)
        if item:
            s3_service.delete_file(item["s3_key"])
            db_service.delete_video(item_id)
            flash("Video deleted successfully", "success")
    else:
        flash("Invalid file type", "error")

    return redirect(url_for("main.browse"))


@bp.route("/api/items/<file_type>")
def api_get_items(file_type):
    """API endpoint to get items (for AJAX)"""
    if file_type == "notes":
        items = db_service.get_all_notes()
        items = [create_note_from_dict(item) for item in items]
    elif file_type == "images":
        items = db_service.get_all_images()
        items = [create_image_from_dict(item) for item in items]
    elif file_type == "videos":
        items = db_service.get_all_videos()
        items = [create_video_from_dict(item) for item in items]
    else:
        items = []

    # Convert items to dictionaries for JSON serialization
    items_dict = []
    for item in items:
        item_dict = item.__dict__.copy()
        # Remove any private attributes
        item_dict = {k: v for k, v in item_dict.items() if not k.startswith("_")}
        items_dict.append(item_dict)

    return jsonify(items_dict)


@bp.route("/health")
def health_check():
    """Health check endpoint"""
    try:
        # Test S3 connection
        s3_service.list_files(prefix="uploads/")

        # Test DynamoDB connection
        db_service.get_all_notes()

        return jsonify(
            {
                "status": "healthy",
                "services": ["s3", "dynamodb"],
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@bp.route("/download/<file_type>/<item_id>")
def download_item(file_type, item_id):
    """Download a file"""
    if file_type == "note":
        item = db_service.get_note_by_id(item_id)
    elif file_type == "image":
        item = db_service.get_image_by_id(item_id)
    elif file_type == "video":
        item = db_service.get_video_by_id(item_id)
    else:
        flash("Invalid file type", "error")
        return redirect(url_for("main.browse"))

    if not item:
        flash("Item not found", "error")
        return redirect(url_for("main.browse"))

    try:
        # Get the file from S3
        import boto3
        from config import Config

        s3_client = boto3.client(
            "s3",
            endpoint_url=Config.AWS_ENDPOINT_URL,
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_DEFAULT_REGION,
        )

        # Download the file
        response = s3_client.get_object(
            Bucket=Config.S3_BUCKET_NAME,
            Key=item["s3_key"],
        )

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(response["Body"].read())
            tmp_path = tmp_file.name

        # Send the file
        return send_file(
            tmp_path,
            as_attachment=True,
            download_name=item["original_filename"],
            mimetype=item.get("file_type", "application/octet-stream"),
        )

    except Exception as e:
        flash(f"Download failed: {str(e)}", "error")
        return redirect(url_for("main.view_item", file_type=file_type, item_id=item_id))


@bp.route("/search")
def search():
    """Search across all file types"""
    query = request.args.get("q", "").strip()

    if not query:
        return redirect(url_for("main.browse"))

    # Search in all tables
    notes = db_service.search_items("notes", query)
    images = db_service.search_items("images", query)
    videos = db_service.search_items("videos", query)

    # Convert to models
    notes_models = [create_note_from_dict(note) for note in notes]
    images_models = [create_image_from_dict(image) for image in images]
    videos_models = [create_video_from_dict(video) for video in videos]

    # Format file sizes
    for item in notes_models + images_models + videos_models:
        if hasattr(item, "file_size"):
            item.formatted_size = format_file_size(item.file_size)

    return render_template(
        "search_results.html",
        query=query,
        notes=notes_models,
        images=images_models,
        videos=videos_models,
        total_results=len(notes_models) + len(images_models) + len(videos_models),
    )


@bp.route("/api/health/detailed")
def detailed_health_check():
    """Detailed health check for all services"""
    health_data = {
        "timestamp": datetime.now().isoformat(),
        "services": {},
        "overall": "healthy",
    }

    try:
        # Check S3
        buckets = s3_service.s3_client.list_buckets()
        health_data["services"]["s3"] = {
            "status": "healthy",
            "buckets_count": len(buckets.get("Buckets", [])),
            "bucket_exists": any(
                b["Name"] == Config.S3_BUCKET_NAME for b in buckets.get("Buckets", [])
            ),
        }
    except Exception as e:
        health_data["services"]["s3"] = {"status": "unhealthy", "error": str(e)}
        health_data["overall"] = "unhealthy"

    try:
        # Check DynamoDB tables
        tables = db_service.dynamodb.tables.all()
        table_names = [table.name for table in tables]

        required_tables = [
            Config.NOTES_TABLE,
            Config.IMAGES_TABLE,
            Config.VIDEOS_TABLE,
        ]

        health_data["services"]["dynamodb"] = {
            "status": "healthy",
            "tables_count": len(table_names),
            "required_tables": {
                table: table in table_names for table in required_tables
            },
        }
    except Exception as e:
        health_data["services"]["dynamodb"] = {"status": "unhealthy", "error": str(e)}
        health_data["overall"] = "unhealthy"

    return jsonify(health_data)
