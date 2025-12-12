from app import create_app

app = create_app()

# Set secret key if not already set (for development only!)
if not app.secret_key:
    app.secret_key = "dev-secret-key-1234567890"

if __name__ == "__main__":
    print("=" * 50)
    print("Memory Vault Application Starting...")
    print(f"Secret Key: {'Set' if app.secret_key else 'Not Set'}")
    print(f"S3 Endpoint: {app.config['AWS_ENDPOINT_URL']}")
    print(f"Bucket: {app.config['S3_BUCKET_NAME']}")
    print(
        f"DynamoDB Tables: {app.config['NOTES_TABLE']}, {app.config['IMAGES_TABLE']}, {app.config['VIDEOS_TABLE']}"
    )
    print("=" * 50)

    app.run(host="0.0.0.0", port=5000, debug=True)
