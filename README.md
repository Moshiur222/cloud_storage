# Mini Cloud Storage System (Backend)

## 📝 Project Description
This is a mini cloud storage backend system built with Django + Django REST Framework.  
It allows users to:
- Upload files (with deduplication)
- Delete files
- View storage summary
- List all uploaded files

**Features:**
- Each user has 500MB storage limit
- Concurrent upload safe
- File deduplication based on file_hash
- UUID based primary keys (secure)

---

## ⚙️ Setup Instructions

1. **Clone Project**
```bash
git clone <repo_url>
cd cloud_storage
