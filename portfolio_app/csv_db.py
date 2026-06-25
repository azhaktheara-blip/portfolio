import csv
from pathlib import Path
from django.conf import settings

def _path(name):
    return Path(settings.CSV_DATA_DIR) / f"{name}.csv"

def read_csv(name):
    p = _path(name)
    if not p.exists():
        return []
    with open(p, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def append_csv(name, row):
    p = _path(name)
    exists = p.exists()
    with open(p, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not exists:
            w.writeheader()
        w.writerow(row)

def get_profile():
    rows = read_csv('profile')
    return rows[0] if rows else {}

def get_projects():   return read_csv('projects')
def get_skills():     return read_csv('skills')
def get_experience(): return read_csv('experience')
def get_messages():   return read_csv('messages')

def save_message(name, email, subject, body):
    from datetime import datetime
    append_csv('messages', {
        'name': name, 'email': email,
        'subject': subject, 'body': body,
        'timestamp': datetime.now().isoformat(timespec='seconds'),
    })
