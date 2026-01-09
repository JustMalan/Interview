# Camp Manager (Interview Project)

## Requirements
- Python 3.10+ (3.11 or 3.12 is fine)
- pip

## Setup
```bash
git clone <REPO_URL>
cd <REPO_FOLDER>

python -m venv .venv
# Mac/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
