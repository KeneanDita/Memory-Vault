# Memory Vault 
A secure, personal memory-management app for capturing, organizing, and revisiting important moments, notes, and media.

Memory Vault lets users safely store and retrieve memories (text, images, audio, video). It supports tagging, searching, timelines, and optional sharing, with privacy-first defaults.

## Features

- Add, edit, delete memories  
- Upload images, notes, and video  
- Tagging & full-text search  
- Browse memories by date/timeline  
- Scheduled backups (optional)

## Installation and Usage

### Clone repo

```bash
git clone https://github.com/KeneanDita/Memory-Vault.git
cd Memory-Vault
```

### Create a virtual environment and install dependencies

```bash
python -m venv .venv
./.venv/Scripts/activate # Source .venv/Scripts/activate for MAC/Linux
pip install -r requirements.txt
```

### Create the bucket and tables using the prepared scripts

```bash
pwsh create_bucket.ps1
pwsh create_all_tables.ps1
```

### Run the app

```bash
python ./run.py
```

## Configuration

Create a `.env` with required keys (example):

```env
S3_BUCKET=my-memory-vault
S3_REGION=us-east-1
AWS_ACCESS_KEY_ID=yourkey
AWS_SECRET_ACCESS_KEY=yoursecret
```

## Running

* Start backend dev server
* Start frontend dev server
* Visit: `http://localhost:5000`

**Docker option:**

```bash
docker-compose up --build
```


## Environment Variables

Keep secrets out of version control; maintain `.env.example`.

## Contributing

1. Fork repo
2. Create branch: `git checkout -b feature/short-description`
3. Commit: `git commit -m "feat: description"`
4. Push + open PR
5. Add tests for new features

Labels: `good first issue`, `bug`, `enhancement`

## License

MIT License - see [LICENSE](LICENSE)

### Contact

**Maintainer:** [Kenean Dita](https://github.com/KeneanDita)
, Questions/issues: open a GitHub issue
