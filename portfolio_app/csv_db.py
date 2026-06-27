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

def write_csv(name, rows, fieldnames=None):
    p = _path(name)
    if not rows:
        open(p, 'w').close()
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    with open(p, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

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

PROFILE_FIELDS = ['name','title','tagline','bio','email','phone','location','github','linkedin','twitter','avatar']
PROJECT_FIELDS = ['id','title','description','tech','demo_url','github_url','image','featured','category']
SKILL_FIELDS   = ['name','level','category','icon']
EXP_FIELDS     = ['id','company','role','period','description','current']
MSG_FIELDS     = ['name','email','subject','body','timestamp']

def save_profile(data):    write_csv('profile',     [data], PROFILE_FIELDS)
def write_projects(rows):  write_csv('projects',    rows,   PROJECT_FIELDS)
def write_skills(rows):    write_csv('skills',      rows,   SKILL_FIELDS)
def write_experience(rows):write_csv('experience',  rows,   EXP_FIELDS)
def write_messages(rows):  write_csv('messages',    rows,   MSG_FIELDS)

def save_message(name, email, subject, body):
    from datetime import datetime
    append_csv('messages', {
        'name': name, 'email': email,
        'subject': subject, 'body': body,
        'timestamp': datetime.now().isoformat(timespec='seconds'),
    })