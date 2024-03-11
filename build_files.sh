# build_files.sh
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py collectstatic