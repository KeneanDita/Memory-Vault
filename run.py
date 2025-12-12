from app import create_app

app = create_app()

if __name__ == "__main__":
    print("Memory Vault Application Starting...")
    print("S3 Endpoint:", app.config["AWS_ENDPOINT_URL"])
    print("Bucket:", app.config["S3_BUCKET_NAME"])
    print(
        "DynamoDB Tables:",
        {
            "notes": app.config["NOTES_TABLE"],
            "images": app.config["IMAGES_TABLE"],
            "videos": app.config["VIDEOS_TABLE"],
        },
    )

    app.run(host="0.0.0.0", port=5000, debug=True)
