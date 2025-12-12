# Memory Vault 🗄️

A robust Flask-based web application for storing and managing your digital memories including notes, images, and videos. Memory Vault provides a secure, organized way to upload, browse, search, and download your important files with metadata tracking and cloud storage capabilities.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.1.2-green.svg)

## ✨ Features

- **Multi-Format Support**: Upload and manage three types of content:
  - 📝 **Notes**: PDFs, text files, Word documents, PowerPoint presentations, Excel spreadsheets, and OpenDocument formats
  - 🖼️ **Images**: PNG, JPG, JPEG, WebP, SVG, GIF, BMP, and TIFF formats
  - 🎥 **Videos**: MP4, MKV, AVI, MOV, WMV, FLV, WebM, and MPEG formats

- **Smart Organization**:
  - Title and description metadata for all files
  - Automatic file type detection and validation
  - Image dimension extraction
  - File size tracking and formatted display
  - Timestamp tracking (created/updated dates)

- **Powerful Search**: 
  - Search across all file types
  - Filter by title and description
  - Tab-based browsing by category

- **User-Friendly Interface**:
  - Clean, responsive web interface
  - Real-time file upload with validation
  - Preview and download capabilities
  - Statistics dashboard showing storage metrics

- **Cloud-Native Architecture**:
  - S3-compatible object storage
  - DynamoDB for metadata persistence
  - LocalStack support for local development
  - Docker and Docker Compose ready

- **Health Monitoring**:
  - Basic health check endpoint
  - Detailed service health monitoring
  - Connection testing for S3 and DynamoDB

## 🛠️ Technology Stack

### Backend
- **Python 3.9**: Core programming language
- **Flask 3.1.2**: Web framework
- **Flask-CORS**: Cross-origin resource sharing support

### Storage & Database
- **AWS S3**: Object storage (or LocalStack for local dev)
- **AWS DynamoDB**: NoSQL database for metadata
- **Boto3**: AWS SDK for Python

### File Processing
- **Pillow**: Image processing and dimension extraction
- **python-magic**: MIME type detection
- **filetype**: File type validation

### Infrastructure
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **LocalStack**: Local AWS cloud stack emulation

### Additional Dependencies
- **python-dotenv**: Environment variable management
- **Werkzeug**: WSGI utilities
- **Requests**: HTTP library

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (20.10+) and **Docker Compose** (1.29+) - for containerized deployment
- **Python 3.9+** - for local development
- **AWS CLI** - for LocalStack setup (optional but recommended)
- **Git** - for cloning the repository

## 🚀 Installation & Setup

### Option 1: Docker Compose (Recommended)

This is the easiest way to get started with Memory Vault.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KeneanDita/Memory-Vault.git
   cd Memory-Vault
   ```

2. **Start the application**:
   ```bash
   docker-compose up --build
   ```

   This will:
   - Start LocalStack (S3 and DynamoDB services) on port 4566
   - Build and start the Memory Vault application on port 5000
   - Wait for LocalStack to be healthy before starting the app

3. **Initialize AWS resources** (in a new terminal):
   
   **For Windows (PowerShell)**:
   ```powershell
   .\create_bucket.ps1
   .\create_all_tables.ps1
   ```

   **For Linux/Mac**:
   ```bash
   # Create S3 bucket
   aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket memory-vault --region us-east-1

   # Create DynamoDB tables
   aws dynamodb create-table \
     --table-name MemoryVaultNotes \
     --attribute-definitions AttributeName=note_id,AttributeType=S \
     --key-schema AttributeName=note_id,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST \
     --endpoint-url http://localhost:4566 \
     --region us-east-1

   aws dynamodb create-table \
     --table-name MemoryVaultImages \
     --attribute-definitions AttributeName=image_id,AttributeType=S \
     --key-schema AttributeName=image_id,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST \
     --endpoint-url http://localhost:4566 \
     --region us-east-1

   aws dynamodb create-table \
     --table-name MemoryVaultVideos \
     --attribute-definitions AttributeName=video_id,AttributeType=S \
     --key-schema AttributeName=video_id,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST \
     --endpoint-url http://localhost:4566 \
     --region us-east-1
   ```

4. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

### Option 2: Local Development Setup

For development without Docker:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KeneanDita/Memory-Vault.git
   cd Memory-Vault
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up LocalStack** (in a separate terminal):
   ```bash
   docker run -d -p 4566:4566 localstack/localstack
   ```

5. **Initialize AWS resources** (follow step 3 from Docker Compose option)

6. **Create a `.env` file** (optional):
   ```env
   SECRET_KEY=your-secret-key-here
   AWS_ENDPOINT_URL=http://localhost:4566
   AWS_ACCESS_KEY_ID=test
   AWS_SECRET_ACCESS_KEY=test
   AWS_DEFAULT_REGION=us-east-1
   S3_BUCKET_NAME=memory-vault
   NOTES_TABLE=MemoryVaultNotes
   IMAGES_TABLE=MemoryVaultImages
   VIDEOS_TABLE=MemoryVaultVideos
   ```

7. **Run the application**:
   ```bash
   python run.py
   ```

8. **Access the application**:
   Open your browser and navigate to: `http://localhost:5000`

## ⚙️ Configuration

Memory Vault uses environment variables for configuration. All settings have sensible defaults for local development.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `dev-secret-key-change-in-production` |
| `AWS_ENDPOINT_URL` | AWS endpoint (LocalStack for dev) | `http://localhost:4566` |
| `AWS_ACCESS_KEY_ID` | AWS access key | `test` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | `test` |
| `AWS_DEFAULT_REGION` | AWS region | `us-east-1` |
| `S3_BUCKET_NAME` | S3 bucket name | `memory-vault` |
| `NOTES_TABLE` | DynamoDB table for notes | `MemoryVaultNotes` |
| `IMAGES_TABLE` | DynamoDB table for images | `MemoryVaultImages` |
| `VIDEOS_TABLE` | DynamoDB table for videos | `MemoryVaultVideos` |

### File Upload Limits

- **Maximum file size**: 100MB
- **Allowed extensions**:
  - **Notes**: pdf, txt, doc, docx, ppt, pptx, xls, xlsx, odt, ods, odp
  - **Images**: png, jpg, jpeg, webp, svg, gif, bmp, tiff
  - **Videos**: mp4, mkv, avi, mov, wmv, flv, webm, mpeg, mpg

## 📖 Usage Guide

### Uploading Files

1. Navigate to the **Upload** page from the home screen
2. Select the file type tab (Notes, Images, or Videos)
3. Fill in the metadata:
   - **Title**: A descriptive title for your file
   - **Description**: Additional details or notes
4. Choose your file using the file picker
5. Click **Upload** to store your file

### Browsing Files

1. Navigate to the **Browse** page
2. Use the tabs to switch between Notes, Images, and Videos
3. Use the search bar to find specific files by title or description
4. Click on any item to view details
5. Download or delete files as needed

### Viewing Statistics

Access the **Statistics** page to see:
- Total number of files by category
- Total storage used per category
- Overall storage metrics

### Searching

Use the global search feature to find files across all categories simultaneously.

## 🔌 API Endpoints

Memory Vault provides several API endpoints for programmatic access:

### Web Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Home page with overview |
| GET/POST | `/upload` | Upload new files |
| GET | `/browse` | Browse all files |
| GET | `/view/<file_type>/<item_id>` | View specific item details |
| POST | `/delete/<file_type>/<item_id>` | Delete an item |
| GET | `/download/<file_type>/<item_id>` | Download a file |
| GET | `/search` | Search across all files |
| GET | `/stats` | View statistics dashboard |

### API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/items/<file_type>` | Get all items of a type (JSON) |
| GET | `/health` | Basic health check |
| GET | `/api/health/detailed` | Detailed service health check |

### Example API Usage

**Get all images**:
```bash
curl http://localhost:5000/api/items/images
```

**Health check**:
```bash
curl http://localhost:5000/health
```

**Detailed health check**:
```bash
curl http://localhost:5000/api/health/detailed
```

## 📁 Project Structure

```
Memory-Vault/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Data models (Note, Image, Video)
│   ├── routes.py                # Route handlers and controllers
│   ├── s3_service.py            # S3 storage service
│   ├── dynamodb_service.py      # DynamoDB database service
│   ├── utils.py                 # Utility functions
│   ├── static/                  # Static assets (CSS, JS)
│   │   ├── css/
│   │   └── js/
│   └── templates/               # Jinja2 HTML templates
│       ├── base.html
│       ├── index.html
│       ├── upload.html
│       ├── browse.html
│       ├── view_content.html
│       ├── stats.html
│       └── components/
├── config.py                    # Configuration management
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker image definition
├── dockercompose.yml           # Docker Compose configuration
├── create_bucket.ps1           # S3 bucket creation script
├── create_all_tables.ps1       # DynamoDB tables creation script
├── .dockerignore               # Docker ignore file
├── .gitignore                  # Git ignore file
├── LICENSE                     # MIT License
└── README.md                   # This file
```

### Key Components

#### Models (`app/models.py`)
- `BaseFile`: Base dataclass for all file types
- `Note`: Model for notes/documents with tags support
- `Image`: Model for images with dimension and EXIF data
- `Video`: Model for videos with duration and resolution
- Factory functions for creating models from DynamoDB items

#### Services
- **S3Service** (`app/s3_service.py`): Handles file upload, download, and deletion in S3
- **DynamoDBService** (`app/dynamodb_service.py`): Manages CRUD operations for metadata in DynamoDB

#### Utils (`app/utils.py`)
- File type validation
- MIME type detection
- Image dimension extraction
- File size formatting
- File extension checking

## 🔧 Development

### Running Tests

Currently, this project doesn't have a test suite. To add tests:

```bash
# Install pytest
pip install pytest pytest-flask

# Create tests directory
mkdir tests

# Run tests
pytest
```

### Code Style

The project follows Python best practices:
- PEP 8 style guide
- Type hints where applicable
- Docstrings for functions and classes

### Adding New Features

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test thoroughly with LocalStack
4. Submit a pull request

### Debugging

Enable debug mode by setting `debug=True` in `run.py` (already enabled by default in development).

View logs:
```bash
# Docker Compose logs
docker-compose logs -f memoryvault

# LocalStack logs
docker-compose logs -f localstack
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Contribution Guidelines

- Write clear, descriptive commit messages
- Add comments for complex logic
- Update documentation for new features
- Ensure code follows existing style conventions
- Test your changes thoroughly

## 🐛 Troubleshooting

### Common Issues

**LocalStack not responding**:
```bash
# Check if LocalStack is running
docker ps | grep localstack

# Restart LocalStack
docker-compose restart localstack
```

**Tables not found**:
```bash
# Verify tables exist
aws dynamodb list-tables --endpoint-url http://localhost:4566 --region us-east-1

# Recreate tables if needed
./create_all_tables.ps1  # Windows
# or use the AWS CLI commands from installation steps
```

**Bucket not found**:
```bash
# Verify bucket exists
aws s3 ls --endpoint-url http://localhost:4566

# Recreate bucket if needed
./create_bucket.ps1  # Windows
```

**File upload fails**:
- Check file size (must be < 100MB)
- Verify file extension is in allowed list
- Ensure LocalStack is running and healthy

**Port already in use**:
```bash
# Change ports in dockercompose.yml
# For the app, change "5000:5000" to "5001:5000"
# For LocalStack, change "4566:4566" to "4567:4566"
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Kenean Dita**

- GitHub: [@KeneanDita](https://github.com/KeneanDita)

## 🙏 Acknowledgments

- Flask team for the excellent web framework
- AWS for S3 and DynamoDB services
- LocalStack team for local AWS emulation
- The open-source community

## 🔮 Future Enhancements

Potential improvements for future releases:

- [ ] User authentication and authorization
- [ ] Multi-user support with access controls
- [ ] File sharing via public links
- [ ] Thumbnail generation for images and videos
- [ ] Video duration and resolution detection
- [ ] EXIF data extraction for images
- [ ] Advanced filtering and sorting options
- [ ] Bulk upload and delete operations
- [ ] File versioning
- [ ] API rate limiting
- [ ] Comprehensive test suite
- [ ] CI/CD pipeline
- [ ] Production deployment guide (AWS, Azure, GCP)
- [ ] Real-time upload progress tracking
- [ ] File preview without downloading
- [ ] Tag-based organization
- [ ] Favorite/starred items
- [ ] Activity logging and audit trails

---

**Note**: This application is designed for local development and testing with LocalStack. For production deployment, you'll need to configure it to use actual AWS services and implement proper security measures including:
- HTTPS/SSL certificates
- Strong secret key management
- AWS IAM roles and policies
- Input validation and sanitization
- Rate limiting and DDoS protection
- Regular security audits
